from prefect import flow, task

@task
def train_model_task():
    print("Training ML model in a dedicated flow...")
    # Placeholder for actual model training logic
    pass

@flow
def model_training_pipeline():
    train_model_task()

if __name__ == "__main__":
    model_training_pipeline()
