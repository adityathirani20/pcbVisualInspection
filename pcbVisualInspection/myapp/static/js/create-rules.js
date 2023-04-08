// Get the select boxes for trained models and inspection type
const trainedModelSelect = document.getElementById('trained_model');
const inspectionTypeSelect = document.getElementById('inspection_type');

// Get the row template
const rowTemplate = document.getElementById('row-template');

// Add event listeners to the select boxes
trainedModelSelect.addEventListener('change', loadSubSelections);
inspectionTypeSelect.addEventListener('change', loadSubSelections);

// Function to load the subselections based on the selected trained model and inspection type
function loadSubSelections() {
  // Get the selected trained model and inspection type
  const trainedModel = trainedModelSelect.value;
  const inspectionType = inspectionTypeSelect.value;

  // Send an AJAX request to the server to get the subselections
  $.ajax({
    url: '/get_subselections/',
    type: 'GET',
    data: {
      'trained_model': trainedModel,
      'inspection_type': inspectionType
    },
    success: function(response) {
      // Remove any existing rows
      const rowsContainer = document.getElementById('rows-container');
      rowsContainer.innerHTML = '';

      // Add a row for each subselection
      response.subselections.forEach(subselection => {
        // Clone the row template
        const row = rowTemplate.content.cloneNode(true).querySelector('tr');

        // Set the label
        const labelSelect = row.querySelector('.label-select');
        subselection.labels.forEach(label => {
          const option = document.createElement('option');
          option.value = label;
          option.text = label;
          labelSelect.appendChild(option);
        });

        // Set the detection checkbox
        const detectionCheckbox = row.querySelector('.detection-checkbox');
        detectionCheckbox.checked = subselection.detection;

        // Set the action select
        const actionSelect = row.querySelector('.action-select');
        subselection.actions.forEach(action => {
          const option = document.createElement('option');
          option.value = action;
          option.text = action;
          actionSelect.appendChild(option);
        });

        // Add the row to the rows container
        rowsContainer.appendChild(row);
      });
    },
    error: function(error) {
      console.log(error);
    }
  });
}

// Add event listener to the add row button
const addRowButton = document.getElementById('add-row-button');
addRowButton.addEventListener('click', function() {
  // Clone the row template
  const row = rowTemplate.content.cloneNode(true).querySelector('tr');

  // Add the row to the rows container
  const rowsContainer = document.getElementById('rows-container');
  rowsContainer.appendChild(row);
});
