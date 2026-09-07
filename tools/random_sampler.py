import pandas as pd
import numpy as np
def calculate_sample_size(N,confidence_level=0.95,margin_of_error=0.05,expected_proportion=0.5):
    """
    Calculates the required sample size based on statistical audit sampling rules.
    Enforces 100% testing for small populations (N <= 10) and scales down to ~0.25% 
    for large populations according to statistical confidence formulas.
    """
    if N<=10:
        return N  #100% sampling rule for small populations

    #Z-scores for standard confidence levels
    z_map={0.90:1.645,0.95:1.96,0.99:2.576}
    Z=z_map.get(confidence_level,1.96)
    p=expected_proportion
    e=margin_of_error
    
    #Infinite population formula (Cochran)
    n_0=(Z**2*p*(1-p))/(e**2)
    
    #Adjust for finite population
    n=n_0/(1+((n_0-1)/N))
    
    #Cap between minimum 10 items and max total population
    return min(N,max(10,int(np.ceil(n))))

def perform_audit_sampling(input_csv,output_csv,confidence_level=0.95,margin_of_error=0.05,random_seed=None):
    """
    Reads population from input CSV, calculates exact sample size, 
    selects items randomly, and saves to output CSV.
    """
    print(f"Loading population data from: {input_csv}...")
    df=pd.read_csv(input_csv)
    population_size=len(df)
    if population_size==0:
        print("Error: Input CSV file is empty.")
        return
    sample_size=calculate_sample_size(
        N=population_size, 
        confidence_level=confidence_level, 
        margin_of_error=margin_of_error
    )
    sample_rate=(sample_size/population_size)*100
    print("\n--- AUDIT SAMPLING SUMMARY ---")
    print(f"Total Population Size (N): {population_size:,}")
    print(f"Target Confidence Level : {confidence_level*100:.0f}%")
    print(f"Target Margin of Error  : {margin_of_error*100:.1f}%")
    print(f"Calculated Sample Size(n): {sample_size:,}")
    print(f"Effective Sampling Rate : {sample_rate:.2f}%")
    print("-------------------------------\n")
    
    #Select random sample without replacement
    sample_df=df.sample(n=sample_size,random_state=random_seed).reset_index(drop=True)
    
    #Add audit tracking column
    sample_df['Audit_Sample_Flag']='Selected'
    
    #Save selected sample to output CSV
    sample_df.to_csv(output_csv,index=False)
    print(f"Successfully exported {len(sample_df):,} sampled rows to: {output_csv}")


if __name__ == '__main__':
    #Example usage:
    perform_audit_sampling(
        input_csv='population_data.csv',
        output_csv='audit_sample_output.csv',
        confidence_level=0.95,   #95% Confidence Level
        margin_of_error=0.05,    #5% Margin of Error
        random_seed=42          #Set seed for reproducible audit workpapers
    )
