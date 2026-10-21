"""Validate the CSV tables consumed by the application."""
if __package__:
    from .data_utils import validate_dataset
else:
    from data_utils import validate_dataset

if __name__ == "__main__":
    for name, frame in validate_dataset().items():
        print(f"{name}: OK ({len(frame)} rows)")
    print("Dataset structure and reference checks completed. Source accuracy is not checked.")
