from prefect import flow, task

@task
def airbyte_sync():
    # Trigger Airbyte connection sync
    print("Triggering Airbyte sync...")
    pass

@task
def dbt_transform():
    # Run dbt models
    print("Running dbt transformations...")
    pass

@task
def train_ml_model():
    # Train churn prediction model
    print("Training ML model...")
    pass

@flow
def main_pipeline():
    airbyte_sync()
    dbt_transform()
    train_ml_model()

if __name__ == "__main__":
    main_pipeline()
