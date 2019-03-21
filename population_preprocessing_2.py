# Use the dataframe cleaned in population_preprocessing_1.py to create 2 additional dataframe to replace population
pop = pd.read_csv('data/population_data.csv', index_col=0)
pop.drop('village', axis=1, inplace = True)

pop.ward = pop.ward.apply(lambda x: x.lower())
pop.ward = pop.ward.apply(lambda x: x.replace("ward", "").strip() if 'ward' in x else x)
pop.ward = pop.ward.apply(lambda x: [alpha for word in x for alpha in word if (alpha.isalpha() or alpha.isspace())])
pop.ward = pop.ward.apply(lambda x: "".join(x))

# remove strings in the remove list below to match with the main dataframe
remove = ['Urban', 'District', 'City', 'Municipal', 'Town', 'Rural', 'Council', 'TC', 'Township']
pop.district = pop.district.apply(lambda x: [d for d in x.split(' ') if d not in remove])
pop.district = pop.district.apply(lambda x: " ".join(x))
pop.district = pop.district.apply(lambda x: [alpha for word in x for alpha in word if (alpha.isalpha() or alpha.isspace())])
pop.district = pop.district.apply(lambda x: "".join(x).lower())

pop = pop.rename(index=str, columns={"district": "lga"})

pop_for_merge = pop.groupby(['lga', 'ward']).agg('sum')
pop_for_merge.to_csv("pop_for_merge.csv", encoding="utf-8")

# if there are still missing values, replace with median value grouped by 'lga' column
pop_median = pop.groupby(['lga']).agg('median')
pop_median.to_csv('pop_median.csv', encoding="utf-8")
