"""
       Test to execute Ranklib:
       Aims to combine different ranking scores of different baselines with L2R setting,
       for producing final ranking with relevant paragraphs.

       Input :
       e.g. '0 qid:10002 1:0.007477 2:0.000000... 45:0.000000 46:0.007042

       * 0 : true relevance label. (e.g. 0-non, 1-relevant and 2-strong relevant)
       * qid : query id
       * 1 2... 45 46 : features for L2R, each column could be our base ranker score (e.g. TFIDF, BM25 ranker scores)

       Output :
       * A model that trains on each ranker(as features in training set), for final relevant ranking list.
"""

import os

# train on the training data and record the model that performs best on the validation data.
# The training metric is NDCG@10. After training is completed, evaluate the trained model on the test data in ERR@10
exp_1_1 = 'java -jar RankLib-2.1-patched.jar ' \
        '-train MQ2008/Fold1/train.txt ' \
        '-test MQ2008/Fold1/test.txt ' \
        '-validate MQ2008/Fold1/vali.txt ' \
        '-ranker 6 ' \
        '-metric2t NDCG@10 ' \
        '-metric2T ERR@10 ' \
        '-save LambdaMART_md.txt'

exp_1_2 = 'java -jar RankLib-2.1-patched.jar ' \
        '-train MQ2008/Fold1/train.txt ' \
        '-test MQ2008/Fold1/test.txt ' \
        '-validate MQ2008/Fold1/vali.txt ' \
        '-ranker 4 ' \
        '-metric2t MAP@10 ' \
        '-metric2T MAP@10 ' \
        '-save CoordinateAscent_md.txt'

# evaluate the pre-trained model stored in mymodel.txt on the specified test data
exp_2 = 'java -jar RankLib-2.1-patched.jar ' \
        '-load mymodel.txt ' \
        '-test MQ2008/Fold1/test.txt ' \
        '-metric2T ERR@10'

# 5-fold cross validation
exp_3 = 'java -jar RankLib-2.1-patched.jar ' \
        '-train MQ2008/Fold1/train.txt ' \
        '-ranker 4 ' \
        '-kcv 5 -kcvmd models/ -kcvmn ca ' \
        '-metric2t NDCG@10 -metric2T ERR@10'

# comparing trained models with test data and save the result
exp_4_1 = 'java -jar RankLib-2.1-patched.jar -test MQ2008/Fold1/test.txt -metric2T NDCG@10 -idv output/baseline.ndcg.txt '
exp_4_2 = 'java -jar RankLib-2.1-patched.jar -load LambdaMART_md.txt -test MQ2008/Fold1/test.txt -metric2T NDCG@10 -idv output/lm.ndcg.txt '
exp_4_3= 'java -jar RankLib-2.1-patched.jar -load CoordinateAscent_md.txt -test MQ2008/Fold1/test.txt -metric2T NDCG@10 -idv output/ca.ndcg.txt'

# Save the result comparing into analysis.txt
exp_4_4 = 'java -cp RankLib-2.1-patched.jar ciir.umass.edu.eval.Analyzer -all output/ -base baseline.ndcg.txt > analysis.txt'

test_1 = 'java -jar RankLib-2.1-patched.jar ' \
        '-train input_for_L2R/input_train.txt ' \
        '-test input_for_L2R/input_test.txt ' \
        '-ranker 4 ' \
        '-metric2t MAP@10 ' \
        '-metric2T MAP@10 ' \
        '-save CoordinateAscent_md.txt'

save_re_ranking = 'java -jar RankLib-2.1-patched.jar ' \
                  '-load CoordinateAscent_md.txt -rank input_for_L2R/input_test.txt -score re_ranking_result.txt'

print('-----Start-----')
# run experiments
os.system(save_re_ranking)