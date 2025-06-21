import numpy as np
import pandas as pd

class LifeExpectancyCalculator:
    """
    A model class for the Life Expectancy Calculator.
    """
    name = "Life Expectancy Calculator"
    description = "Estimate your life expectancy based on various factors."

    @staticmethod
    def calculate(age, income, smoking, drinking, exercise, region, height, weight, gender, medical_history):
        """
        Estimate life expectancy based on user inputs.

        Parameters:
        - age: Current age of the individual
        - income: Annual income in USD
        - smoking: Smoking frequency (0=Never, 1=Occasionally, 2=Regularly)
        - drinking: Drinking frequency (0=Never, 1=Occasionally, 2=Regularly)
        - exercise: Exercise frequency (0=Never, 1=Occasionally, 2=Regularly)
        - region: Country name
        - height: Height in centimeters
        - weight: Weight in kilograms
        - gender: Gender of the individual ("Male" or "Female")
        - medical_history: List of chronic diseases (e.g., ["diabetes", "hypertension"])

        Returns:
        - Estimated life expectancy
        """
        # Initialize region_factor to avoid UnboundLocalError
        region_factor = 0  # Default value before extracting from country data

        # Adjust base life expectancy to align with country-specific total life expectancy
        base_life_expectancy = region_factor - 20  # Reduce base life expectancy further

        # Comprehensive validation and cleanup
        # Load country data with the correct delimiter
        country_data = pd.read_csv("data/life/life2025.csv", sep='\s+')
        country_data.columns = country_data.columns.str.strip().str.replace('"', '')

        # Ensure 'Country' column exists
        if 'Country' not in country_data.columns:
            raise ValueError("The CSV file does not have a 'Country' column.")
        country_data['Country'] = country_data['Country'].str.strip()

        # Dynamically create 'LifeExpectancyAdjustment' column based on gender
        if gender == "Male" and 'Males' in country_data.columns:
            country_data['LifeExpectancyAdjustment'] = country_data['Males']
        elif gender == "Female" and 'Females' in country_data.columns:
            country_data['LifeExpectancyAdjustment'] = country_data['Females']
        else:
            raise ValueError("The CSV file does not have the required gender column to calculate 'LifeExpectancyAdjustment'.")

        # Dynamically create missing columns with default values or derived logic
        if 'HealthcareQuality' not in country_data.columns:
            country_data['HealthcareQuality'] = 50  # Default value for healthcare quality
        if 'PollutionLevel' not in country_data.columns:
            country_data['PollutionLevel'] = 30  # Default value for pollution level
        if 'ObesityRate' not in country_data.columns:
            country_data['ObesityRate'] = (
                country_data['Females'] + country_data['Males']
            ) / 2 * 0.1  # Example derived logic for obesity rate

        # Clean region input to match country names
        region = region.strip()

        # Match country data
        country_row = country_data[country_data['Country'] == region]

        if country_row.empty:
            raise ValueError(f"Region '{region}' not found in the CSV file.")

        # Extract region-specific factors
        region_factor = country_row.iloc[0]["LifeExpectancyAdjustment"]
        healthcare_quality = country_row.iloc[0]["HealthcareQuality"]
        pollution_level = country_row.iloc[0]["PollutionLevel"]
        obesity_rate = country_row.iloc[0]["ObesityRate"]

        # Adjustments based on age
        age_factor = max(0, (base_life_expectancy - age))

        # Adjustments based on smoking
        smoking_factor = -10 * smoking  # Increase negative impact of smoking

        # Adjustments based on drinking
        drinking_factor = -7 * drinking  # Increase negative impact of drinking

        # Adjustments based on income
        income_factor = (np.log(max(1, income)) - 10) * 0.5  # Further reduce positive impact of income

        # Adjustments based on exercise
        exercise_factor = 2 * exercise  # Reduce positive impact of exercise

        # Adjustments based on BMI
        bmi = weight / ((height / 100) ** 2) if height > 0 else 0  # Calculate BMI
        bmi_factor = -0.2 * (bmi - 22) ** 2  # Increase negative impact of BMI deviation

        # Adjustments based on healthcare quality
        healthcare_factor = healthcare_quality * 0.3  # Further reduce positive impact of healthcare quality

        # Adjustments based on pollution level
        pollution_factor = -pollution_level * 0.5  # Increase negative impact of pollution level

        # Adjustments based on obesity rate
        obesity_factor = -obesity_rate * 0.4  # Increase negative impact of obesity rate

        # Adjustments based on chronic diseases and medical history
        chronic_disease_factor = 0
        if "diabetes" in medical_history:
            chronic_disease_factor -= 10
        if "hypertension" in medical_history:
            chronic_disease_factor -= 8
        if "heart_disease" in medical_history:
            chronic_disease_factor -= 15

        # Adjustments based on gender
        if gender == "Male":
            base_life_expectancy += 0  # Neutral adjustment for males
        elif gender == "Female":
            base_life_expectancy += 3  # Slight positive adjustment for females

        # Introduce randomness with a normal distribution
        random_factor = np.random.normal(loc=0, scale=5)  # Mean 0, standard deviation 5

        # Calculate final life expectancy with randomness
        estimated_life_expectancy = (
            age_factor + income_factor + smoking_factor + drinking_factor + 
            exercise_factor + region_factor + bmi_factor + healthcare_factor + 
            pollution_factor + obesity_factor + chronic_disease_factor + random_factor
        )

        # Cap the total life expectancy to a maximum of 120 years
        total_life_expectancy = min(120, age + estimated_life_expectancy)

        # Ensure the method returns both remaining and total life expectancy
        return {
            "remaining_life_expectancy": max(0, total_life_expectancy - age),
            "total_life_expectancy": total_life_expectancy
        }
