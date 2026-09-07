import pandas as pd
import numpy as np

def determine_sample_size(population_size):
    """
    Determines standard internal audit sample size based on population thresholds.
    """
    if population_size<10:
        return population_size  #100% testing
    elif 10<=population_size<=50:
        return min(population_size,max(5,int(population_size*0.20)))
    elif 50<population_size<=250:
        return min(population_size,max(10,int(population_size*0.10)))
    else:  #>250 items
        #Capped between 25 and 60 items for continuous / large populations
        return min(population_size,max(25,min(60,int(population_size*0.05))))

def extract_audit_sample(df,random_state=None):
    """
    Extracts a random audit sample from a pandas DataFrame.
    """
    pop_size=len(df)
    if pop_size==0:
        raise ValueError("The provided dataset is empty.")
    
    sample_size=determine_sample_size(pop_size)
    sample_df=df.sample(n=sample_size,random_state=random_state)
    
    return sample_df,sample_size


#Example Usage:
if __name__ =="__main__":
    #1. Load population data from your CSV file
    df_population=pd.read_csv("your_csv_population_sample_file.csv")
    
    #2. Extract sample
    sampled_data,n_samples=extract_audit_sample(df_population,random_state=42)
    
    print(f"Total Population: {len(df_population)}")
    print(f"Sample Size Taken: {n_samples}")
    print("\nSampled Records:")
    print(sampled_data.head())


    #3. Save sample to CSV
    sampled_data.to_csv("your_sampling_output.csv",index=False)