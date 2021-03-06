## Steps to run full analysis


#### Part 1: Prep

1. `split_csv_to_txt.py` to split the original `.csv` file into 5 `.txt` files (one for each rating level).
2. `tokenize_english.py` to run spaCy tokenization and lemmatization.
3. `sample_random_lemmas.py` to select random lemmas for the control group.
    Other specific lemmas for study should also be selected here.
4. (optional) `stats.py` to show info about how many tokens there are.


#### Part 2: Automated analysis

1. `tf_idf.py` to calculate all TF-IDF scores.
2. `tf_idf_slope.py` to calculate all slopes of TF-IDF scores relative to number of stars.
3. `automated_final.py` to calculate all final automated scores for eac
4. `search_scores.py` to grab scores for the targeted words.


#### Part 3: Manual analysis

1. `print_context.py` to find all instances of each lemma in context.
2. `manual_scoring.py` to manually assign scores to sampled context instances.


#### Part 4: Correlation between Automated and Manual scores

1. `final_analysis.py` to run a regression analysis on each of the groups.
