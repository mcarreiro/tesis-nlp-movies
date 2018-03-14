# coding: utf-8
import pickle
from config import *
import numpy as np
from scipy.sparse import coo_matrix, lil_matrix
from scipy.sparse.linalg import svds
import pandas as pd
from Tokenizer import Tokenizer
import gc
from scipy.stats import fisher_exact

tokenizer = Tokenizer()

YEAR_RANGES = [list(range(e, e + 10)) for e in list(range(1967, 2017, 10))]

class CooccurrenceMatrix(object):

    def __init__(self, subs_ids, length, min_freq):

        self.length = length
        self.min_freq = min_freq
        self.n_subs = subs_ids.shape[0]

        # Get appearances of tokens by year
        self.index = {}
        for i, row in enumerate(subs_ids.itertuples()):
            year = int(row.imdb_year)
            with open(datasets_path + "contexts/%02d/%s_tokens.p" % (self.length, str(int(row.sub_id))), "rb") as f:
                tokens = pickle.load(f)
            for token in tokens:
                if token not in self.index:
                    self.index[token] = {}
                if year not in self.index[token]:
                    self.index[token][year] = 0
                self.index[token][year] += 1

        # Get lemmas
        self.lemmas = dict(zip(self.index, tokenizer.lemmatize(self.index)))

        # Get appearances of lemmas by year
        self.lemmatized_index = {}
        for t, l in self.lemmas.items():
            if l not in self.lemmatized_index:
                self.lemmatized_index[l] = {}
            for y in self.index[t]:
                # if y == "total":
                #    continue
                self.lemmatized_index[l][y] = self.lemmatized_index[l].get(y, 0) + self.index[t][y]

        # Get total appearances of lemmas
        for l in self.lemmatized_index:
            # if "total" in self.lemmatized_index[l]:
            #    del self.lemmatized_index[l]["total"]
            self.lemmatized_index[l]["total"] = sum(self.lemmatized_index[l].values())

        # Leave out unfrequent lemmas
        for l in list(self.lemmatized_index):
            if self.lemmatized_index[l]["total"] < self.min_freq:
                del self.lemmatized_index[l]

        self.lemmas_order = dict([(l, i) for (i, l) in enumerate(sorted(self.lemmatized_index))])
        self.lemmas = dict([(t, {"l": l, "order": self.lemmas_order[l]}) for (t, l) in self.lemmas.items() if (l in self.lemmatized_index)])
        self.n_tokens = sum([self.lemmatized_index[e]["total"] for e in self.lemmatized_index])

        # Generate the aggregate contexts
        self.contexts = {}
        self.denom = 0
        for i, s in enumerate([int(e) for e in subs_ids.sub_id]):
            with open(datasets_path + "contexts/%02d/%s_contexts.p" % (self.length, str(int(s))), "rb") as f:
                s_contexts = pickle.load(f)
                # Check that the matrix will be symmetric
                # for t1 in s_contexts:
                #    for t2 in s_contexts[t1]:
                #        assert(s_contexts[t1][t2] == s_contexts[t2][t1])

            for t in s_contexts:
                if t not in self.lemmas:
                    continue
                tl = self.lemmas[t]["l"]
                if tl not in self.contexts:
                    self.contexts[tl] = {}
                for c in s_contexts[t]:
                    if c not in self.lemmas:
                        continue
                    cl = self.lemmas[c]["l"]
                    self.contexts[tl][cl] = self.contexts[tl].get(cl, 0) + s_contexts[t][c]
                    self.denom += s_contexts[t][c]

    def build_cooc_matrix(self):
        rows = []
        cols = []
        freq = []
        for l1 in self.contexts:
            for l2 in self.contexts[l1]:
                rows.append(self.lemmas_order[l1])
                cols.append(self.lemmas_order[l2])
                fij = self.contexts[l1][l2]
                freq.append(fij)

        rows = np.array(rows)
        cols = np.array(cols)
        freq = np.array(freq)

        self.cooc_matrix = coo_matrix((freq, (rows, cols)),
                                      shape=(len(self.lemmas_order),
                                             len(self.lemmas_order)))

    def build_svd(self, dim):  # No está tan revisado
        self.dim = dim + 1
        rows = []
        cols = []
        freq = []
        gw_freq = []
        sorted_lemmas = sorted(self.lemmas_order, key=lambda x: self.lemmas_order[x])
        for l1 in sorted_lemmas:  # Paso por todos los lemas, esté o no
            if l1 not in self.contexts:
                gw_freq.append(1)
                continue
            else:
                acum = 0
                for l2 in self.contexts[l1]:
                    rows.append(self.lemmas_order[l1])
                    cols.append(self.lemmas_order[l2])
                    fij = self.contexts[l1][l2]
                    freq.append(fij)
                    acum += (fij / self.denom) * np.log(fij / self.denom)
                gw_freq.append(1 + ((acum) / np.log(self.n_subs)))

        rows = np.array(rows)
        cols = np.array(cols)
        freq = np.array(freq)
        gw_freq = np.array(gw_freq)
        lw_freq = np.log(freq + 1)  # Local weight

        cooc_matrix = coo_matrix((lw_freq, (rows, cols)),
                                 shape=(len(self.lemmas_order),
                                        len(self.lemmas_order)))

        gw_tmp = lil_matrix((len(self.lemmas_order), len(self.lemmas_order)))
        gw_tmp.setdiag(gw_freq)

        cooc_matrix = gw_tmp * cooc_matrix

        self.U, self.S, self.Vt = svds(cooc_matrix, k=self.dim)

    def ppmi(self, w1, w2, alpha):
        w1 = filter(lambda x: x in self.lemmas, w1)
        v1_loc = []
        for l in w1:
            v1_loc.append(self.lemmas[l]["order"])

        w2 = filter(lambda x: x in self.lemmas, w2)
        v2_loc = []
        for l in w2:
            v2_loc.append(self.lemmas[l]["order"])

        csr_matrix = self.cooc_matrix.tocsr()

        if not v1_loc or not v2_loc:
            return None
        else:
            for i, l1 in enumerate(v1_loc):
                if not i:
                    row_sums = csr_matrix.getrow(l1).todense()
                else:
                    row_sums += csr_matrix.getrow(l1).todense()

            for i, l2 in enumerate(v2_loc):
                if not i:
                    col_sums = csr_matrix.getrow(l2).todense()
                else:
                    col_sums += csr_matrix.getrow(l2).todense()

        p_ij = row_sums[0, v2_loc].sum() / csr_matrix.sum()
        p_i = row_sums.sum() / csr_matrix.sum()
        p_j = np.power(col_sums.sum(), alpha) / csr_matrix.power(alpha).sum()

        return(0 if (p_ij == 0) else max(np.log2(p_ij / (p_i * p_j)), 0))

    def dist_svd(self, w1, w2, dim=300):

        # Set vector to norm 1
        U = np.delete(self.U, [0], axis=1)
        U = U[:, range(dim)]
        U = U / np.linalg.norm(U, axis=1).reshape(U.shape[0], 1)

        w1 = filter(lambda x: x in self.lemmas, w1)
        v1_loc = []
        for i, w in enumerate(w1):
            v1_loc.append(self.lemmas[w]["order"])
            if not i:
                v1 = U[v1_loc[-1], :].reshape(dim, 1)
            else:
                v1 += U[v1_loc[-1], :].reshape(dim, 1)
        v1 /= (i + 1)
        v1 = v1 / np.linalg.norm(v1)

        w2 = filter(lambda x: x in self.lemmas, w2)
        v2_loc = []
        for i, w in enumerate(w2):
            v2_loc.append(self.lemmas[w]["order"])
            if not i:
                v2 = U[v2_loc[-1], :].reshape(dim, 1)
            else:
                v2 += U[v2_loc[-1], :].reshape(dim, 1)
        v2 /= (i + 1)
        v2 = v2 / np.linalg.norm(v2)

        U = np.delete(U, v1_loc + v2_loc, axis=0)
        similarities = np.dot(U, v1)

        return (np.dot(v1.T, v2) > similarities).sum() / similarities.size

    def fisher_test(self, w1, w2, w3):
        w1 = filter(lambda x: x in self.lemmas, w1)
        v1_loc = []
        for l in w1:
            v1_loc.append(self.lemmas[l]["order"])

        w2 = filter(lambda x: x in self.lemmas, w2)
        v2_loc = []
        for l in w2:
            v2_loc.append(self.lemmas[l]["order"])

        w3 = filter(lambda x: x in self.lemmas, w3)
        v3_loc = []
        for l in w3:
            v3_loc.append(self.lemmas[l]["order"])

        csr_matrix = self.cooc_matrix.tocsr()

        if not v1_loc or not v2_loc or not v3_loc:
            return None
        else:
            for i, l1 in enumerate(v1_loc):
                if not i:
                    row1_sums = csr_matrix.getrow(l1).todense()
                else:
                    row1_sums += csr_matrix.getrow(l1).todense()

            for i, l2 in enumerate(v2_loc):
                if not i:
                    row2_sums = csr_matrix.getrow(l2).todense()
                else:
                    row2_sums += csr_matrix.getrow(l2).todense()

        w1_and_w3 = row1_sums[:, v3_loc].sum()
        w1_and_not_w3 = row1_sums.sum() - w1_and_w3
        w2_and_w3 = row2_sums[:, v3_loc].sum()
        w2_and_not_w3 = row2_sums.sum() - w2_and_w3

        cont_table = np.array([[w1_and_w3, w1_and_not_w3],
                               [w2_and_w3, w2_and_not_w3]])

        return(fisher_exact(cont_table)[1])

    def w_freq(self, w1):
        freq = 0
        for w in w1:
            if w in self.lemmatized_index:
                freq += self.lemmatized_index[w]["total"]
        return freq / self.n_tokens


if __name__ == "__main__":

    def create_embeddings(length, sample, svd=False, ppmi=False):
        top_movies = pd.read_csv(datasets_path + "filtered_index.txt", sep="\t")
        top_movies["imdb_genre"] = [eval(e) if not isinstance(e, float) else np.nan for e in top_movies.imdb_genre]

        if sample == "family":
            mask = [((not isinstance(e, float)) and (("Family" in e) or ("Animation" in e))) for e in top_movies.imdb_genre]
            top_movies = top_movies[mask]

        # By 5 year periods
        for y in YEAR_RANGES:
            print(y)
            mask = top_movies.sub_id.notnull()
            mask = mask & (top_movies.imdb_year.isin(set(y)))
            subs_ids = top_movies.loc[mask]

            cm = CooccurrenceMatrix(subs_ids, length, min_freq=1)

            if svd:
                cm.build_svd(300)
                with open(datasets_path + "cooccurrence_matrices/svd/%s/%02d/%d.p" % (sample, length, y[0]), "wb") as f:
                    pickle.dump(cm, f)

            if ppmi:
                cm.build_cooc_matrix()
                with open(datasets_path + "cooccurrence_matrices/ppmi/%s/%02d/%d.p" % (sample, length, y[0]), "wb") as f:
                    pickle.dump(cm, f)

        # 2000 onwards
        y = range(2010, 2017)
        print(y)
        mask = top_movies.sub_id.notnull()
        mask = mask & (top_movies.imdb_year.isin(set(y)))
        subs_ids = top_movies.loc[mask]

        cm = CooccurrenceMatrix(subs_ids, length, min_freq=1)

        if svd:
            cm.build_svd(300)
            with open(datasets_path + "cooccurrence_matrices/svd/%s/%02d/2000_onwards.p" % (sample, length), "wb") as f:
                pickle.dump(cm, f)

        if ppmi:
            cm.build_cooc_matrix()
            with open(datasets_path + "cooccurrence_matrices/ppmi/%s/%02d/2000_onwards.p" % (sample, length), "wb") as f:
                pickle.dump(cm, f)

    def load_embeddings(length, sample, metric):
        embeddings = {}
        for y in YEAR_RANGES:
            print(y[0])
            if metric == "svd":
                with open(datasets_path + "cooccurrence_matrices/svd/%s/%02d/%d.p" % (sample, length, y[0]), "rb") as f:
                    emb_tmp = pickle.load(f)
                emb_tmp.n_tokens = sum([emb_tmp.lemmatized_index[e]["total"] for e in emb_tmp.lemmatized_index])
                embeddings[y[0]] = emb_tmp
                del embeddings[y[0]].contexts
                del embeddings[y[0]].S
                del embeddings[y[0]].lemmas_order
                del embeddings[y[0]].Vt
            elif metric == "ppmi":
                with open(datasets_path + "cooccurrence_matrices/ppmi/%s/%02d/%d.p" % (sample, length, y[0]), "rb") as f:
                    emb_tmp = pickle.load(f)
                emb_tmp.n_tokens = sum([emb_tmp.lemmatized_index[e]["total"] for e in emb_tmp.lemmatized_index])
                embeddings[y[0]] = emb_tmp
                del embeddings[y[0]].contexts
                del embeddings[y[0]].lemmas_order
            gc.collect()

        # 2000 onwards
        if metric == "svd":
            with open(datasets_path + "cooccurrence_matrices/svd/%s/%02d/2000_onwards.p" % (sample, length), "rb") as f:
                emb_tmp = pickle.load(f)
            embeddings["2000_onwards"] = emb_tmp
            del embeddings["2000_onwards"].contexts
            del embeddings["2000_onwards"].S
            del embeddings["2000_onwards"].lemmas_order
            del embeddings["2000_onwards"].Vt
        elif metric == "ppmi":
            with open(datasets_path + "cooccurrence_matrices/ppmi/%s/%02d/2000_onwards.p" % (sample, length), "rb") as f:
                emb_tmp = pickle.load(f)
            embeddings["2000_onwards"] = emb_tmp
            del embeddings["2000_onwards"].contexts
            del embeddings["2000_onwards"].lemmas_order
        gc.collect()
        return embeddings

    def time_evol_svd(embeddings, w1, w2, dim=300):
        evolution = []
        for y in YEAR_RANGES:
            try:
                evolution.append((y[0], embeddings[y[0]].dist_svd(w1, w2, dim)))
            except Exception:
                evolution.append((y[0], None))
        return evolution

    def time_evol_ppmi(embeddings, w1, w2, alpha=0.75):
        evolution = []
        for y in YEAR_RANGES:
            evolution.append((y[0], embeddings[y[0]].ppmi(w1, w2, alpha)))
        return evolution

    def time_evol_chi2(embeddings, w1, w2, w3):
        evolution = []
        for y in YEAR_RANGES:
            evolution.append((y[0], embeddings[y[0]].fisher_test(w1, w2, w3)))
        return evolution

    def gen_evol_table(w1, w2, w3, embeddings, filename):

        dists = zip(time_evol_ppmi(embeddings, w1, w3),
                    time_evol_ppmi(embeddings, w2, w3),
                    time_evol_chi2(embeddings, w1, w2, w3))

        res = ["year\the\tshe\tp_value"]
        for (e1, e2), (e3, e4), (e5, e6) in dists:
            res.append("\t".join([str(e1), str(e2), str(e4), str(e6)]))
        with open(graph_path + "%s.txt" % filename, "w") as f:
            f.write("\n".join(res) + "\n")

    def gen_diff(w1, w2, w3, embeddings, filename, alpha=0.75):

        dists = (embeddings["2000_onwards"].ppmi(w1, w3, alpha),
                 embeddings["2000_onwards"].ppmi(w2, w3, alpha),
                 embeddings["2000_onwards"].fisher_test(w1, w2, w3))

        res = ["he\tshe\tp_value", "\t".join([str(e) for e in dists])]

        with open(graph_path + "%s.txt" % filename, "w") as f:
            f.write("\n".join(res) + "\n")

    def evol_freq(w1, embeddings):
        evol_freq = []
        for y in YEAR_RANGES:
            evol_freq.append((y[0], embeddings[y[0]].w_freq(w1)))
        return evol_freq

    """ Avoid this step if the embeddings are already created
    for l in [15, 45, 30]:
        create_embeddings(l, "full", ppmi=True)
        create_embeddings(l, "family", ppmi=True)
    """

    embeddings_full = load_embeddings(30, "full", metric="ppmi")
    embeddings_family = load_embeddings(30, "family", metric="ppmi")

    # Data for relative evolution
    def relative_evol(embeddings, filename):
        evol_man, evol_fem = evol_freq(male_pronouns, embeddings), evol_freq(female_pronouns, embeddings)
        evol_data = ["year\tn\the\tshe"]
        for e in range(len(evol_man)):
            evol_data.append("\t".join([str(evol_man[e][0]), str(embeddings[evol_man[e][0]].n_subs), str(evol_man[e][1]), str(evol_fem[e][1])]))
        with open(graph_path + "%s.txt" % filename, "w") as f:
            f.write("\n".join(evol_data) + "\n")

    relative_evol(embeddings_full, "evol_freq_full")
    relative_evol(embeddings_family, "evol_freq_family")

    # Data for plot 1-a
    gen_diff(male_pronouns, female_pronouns, masculine_roles, embeddings_full, "mp_fp_mr_fu_diff")
    gen_diff(male_pronouns, female_pronouns, feminine_roles, embeddings_full, "mp_fp_fr_fu_diff")
    gen_diff(male_pronouns, female_pronouns, neutral_roles, embeddings_full, "mp_fp_nr_fu_diff")
    gen_diff(male_pronouns, female_pronouns, masculine_roles, embeddings_family, "mp_fp_mr_fm_diff")
    gen_diff(male_pronouns, female_pronouns, feminine_roles, embeddings_family, "mp_fp_fr_fm_diff")
    gen_diff(male_pronouns, female_pronouns, neutral_roles, embeddings_family, "mp_fp_nr_fm_diff")

    # Data for plot 1-b
    gen_evol_table(male_pronouns, female_pronouns, masculine_roles, embeddings_full, "mp_fp_mr_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, feminine_roles, embeddings_full, "mp_fp_fr_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, neutral_roles, embeddings_full, "mp_fp_nr_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, masculine_roles, embeddings_family, "mp_fp_mr_fm_evol")
    gen_evol_table(male_pronouns, female_pronouns, feminine_roles, embeddings_family, "mp_fp_fr_fm_evol")
    gen_evol_table(male_pronouns, female_pronouns, neutral_roles, embeddings_family, "mp_fp_nr_fm_evol")

    # Data for plot 1-b
    gen_diff(male_pronouns, female_pronouns, smart_words, embeddings_full, "mp_fp_sw_fu_diff")
    gen_diff(male_pronouns, female_pronouns, smart_words, embeddings_family, "mp_fp_sw_fm_diff")

    # Data for plot 2-b
    gen_evol_table(male_pronouns, female_pronouns, smart_words, embeddings_full, "mp_fp_sw_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, smart_words, embeddings_family, "mp_fp_sw_fm_evol")

    # Data for plot S1-a
    gen_diff(male_pronouns, female_pronouns, masculine_traits, embeddings_full, "mp_fp_mt_fu_diff")
    gen_diff(male_pronouns, female_pronouns, feminine_traits, embeddings_full, "mp_fp_ft_fu_diff")
    gen_diff(male_pronouns, female_pronouns, neutral_traits, embeddings_full, "mp_fp_nt_fu_diff")
    gen_diff(male_pronouns, female_pronouns, masculine_traits, embeddings_family, "mp_fp_mt_fm_diff")
    gen_diff(male_pronouns, female_pronouns, feminine_traits, embeddings_family, "mp_fp_ft_fm_diff")
    gen_diff(male_pronouns, female_pronouns, neutral_traits, embeddings_family, "mp_fp_nt_fm_diff")

    # Data for plot S1-b
    gen_evol_table(male_pronouns, female_pronouns, masculine_traits, embeddings_full, "mp_fp_mt_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, feminine_traits, embeddings_full, "mp_fp_ft_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, neutral_traits, embeddings_full, "mp_fp_nt_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, masculine_traits, embeddings_family, "mp_fp_mt_fm_evol")
    gen_evol_table(male_pronouns, female_pronouns, feminine_traits, embeddings_family, "mp_fp_ft_fm_evol")
    gen_evol_table(male_pronouns, female_pronouns, neutral_traits, embeddings_family, "mp_fp_nt_fm_evol")

    # Data for plot S2-a
    gen_diff(male_pronouns, female_pronouns, smart_words_jf, embeddings_full, "mp_fp_swj_fu_diff")
    gen_diff(male_pronouns, female_pronouns, smart_words_jf, embeddings_family, "mp_fp_swj_fm_diff")

    # Data for plot S2-b
    gen_evol_table(male_pronouns, female_pronouns, smart_words_jf, embeddings_full, "mp_fp_swj_fu_evol")
    gen_evol_table(male_pronouns, female_pronouns, smart_words_jf, embeddings_family, "mp_fp_swj_fm_evol")
