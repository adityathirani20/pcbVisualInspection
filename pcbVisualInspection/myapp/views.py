from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os


# Create your views here.

def home(request):
    return render(request, 'home.html')


@csrf_exempt
def upload_dataset(request):
    if request.method == 'POST':

        # Get uploaded files
        images = request.FILES.getlist('images')
        annotations = request.FILES.getlist('annotations')
        yaml_file = request.FILES.get('yaml_file')

        # Get dataset name from form input
        dataset_name = request.POST.get('dataset_name')

        # Check if number of images and annotations match
        if len(images) != len(annotations):
            return HttpResponse("Number of images and annotations do not match.")

        # Create dataset directory
        dataset_dir = os.path.join('datasets', dataset_name)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        # Save images and annotations to dataset directory
        for i in range(len(images)):
            image = images[i]
            annotation = annotations[i]
            if image.name.split('.')[0] != annotation.name.split('.')[0]:
                return HttpResponse("Image and annotation file names do not match.")
            file_name = image.name
            image_path = os.path.join(dataset_dir, file_name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            file_name = annotation.name
            annotation_path = os.path.join(dataset_dir, file_name)
            with open(annotation_path, 'wb+') as destination:
                for chunk in annotation.chunks():
                    destination.write(chunk)

        # Save YAML file to dataset directory
        yaml_file_path = os.path.join(dataset_dir, yaml_file.name)
        with open(yaml_file_path, 'wb+') as destination:
            for chunk in yaml_file.chunks():
                destination.write(chunk)

        # Return success message
        return HttpResponse("Dataset uploaded successfully.")

    # Render upload form
    return render(request, 'upload_dataset.html')


def train_model(request):
    if request.method == 'POST':
        model_type = request.POST.get('model_type')
        datasets = request.POST.getlist('datasets')
        model_name = request.POST.get('model_name')
        base_model_id = request.POST.get('base_model')

        # TODO: Train the model using the selected datasets, model type, model name, and base model (if provided)
        # ...

        return redirect('model_detail', model_name=model_name)
    else:
        datasets = ["a", "b", "c", "d"]
        base_models = ["b1", "b2", "b3", "b4"]
        return render(request, 'train_model.html', {'datasets': datasets, 'base_models': base_models})


def create_rules(request):
    trained_models = ["1", "2", "3", "4"]
    return render(request, 'create_rules.html', {'trained_models': trained_models})


def visual_inspection(request):
    rules = ["Rule 1", "Rule 2", "Rule 3"]
    context = {'rules': rules}
    return render(request, 'visual_inspection.html', context)


def dashboard(request):
    # Get the list of created rules and progress of PCB assembly from the database
    rules = [{
        'name' : 'Rule 1',
        'description' : 'Description 1',
        'status' : 'Done'
    },
        {
            'name': 'Rule 2',
            'description': 'Description 2',
            'status': 'Done'
        },
        {
            'name': 'Rule 3',
            'description': 'Description 2',
            'status': 'InProgress'
        },
        {
                'name': 'Rule 4',
                'description': 'Description 2',
                'status': 'Pending'
        }
    ]
    progress = 75

    context = {
        'rules': rules,
        'progress': progress,
    }

    return render(request, 'dashboard.html', context)


def live_pcb_inspection(request):
    # Your logic for fetching and processing data
    # ...

    todos = [
        {
            'title': 'Assemble PCB',
            'description': 'Assemble all components on PCB',
            'subtasks': [
                {'title': 'Solder resistors', 'status': 'Completed', 'remarks': 'Done on time'},
                {'title': 'Solder capacitors', 'status': 'In progress', 'remarks': 'Need more components'},
                {'title': 'Solder IC', 'status': 'Pending', 'remarks': 'Waiting for delivery'},
            ]
        },
        {
            'title': 'Test PCB',
            'description': 'Test assembled PCB for functionality',
            'subtasks': [
                {'title': 'Test voltage regulator', 'status': 'Completed', 'remarks': 'Working fine'},
                {'title': 'Test microcontroller', 'status': 'In progress', 'remarks': 'Firmware issue'},
                {'title': 'Test sensors', 'status': 'Pending', 'remarks': 'Waiting for components'},
            ]
        }
    ]

    return render(request, 'live_pcb_inspection.html', {'todos' : todos})
