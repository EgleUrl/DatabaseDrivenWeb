document.addEventListener('DOMContentLoaded', function() {
    // Event listener for the make dropdown
    document.getElementById('makeDropdown').addEventListener('change', function() {
        var selectedMake = this.value;
        if (selectedMake) {
            // Makes an AJAX request to the server
            fetch('/get-models/' + encodeURIComponent(selectedMake))
                .then(response => response.json())
                .then(data => {
                    // Calls function to update the model dropdown
                    updateDropdown('modelDropdown', data);
                })
                .catch(error => {
                    console.error('Error fetching models:', error);
                });
        } 
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Event listener for the model dropdown
    document.getElementById('modelDropdown').addEventListener('change', function() {
        var selectedModel = this.value;
        if (selectedModel) {
            // Fetches and update towns
            fetch('/get-towns/' + encodeURIComponent(selectedModel))
                .then(response => response.json())
                .then(data => {
                    updateDropdown('townDropdown', data);
                })
                .catch(error => {
                    console.error('Error fetching towns:', error);
                });
            } 
        if (selectedModel) {    
            // Fetches and update regions
            fetch('/get-regions/' + encodeURIComponent(selectedModel))
                .then(response => response.json())
                .then(data => {
                    updateDropdown('regionDropdown', data);
                })
                .catch(error => {
                    console.error('Error fetching regions:', error);
                });
            
        } 
    });
});

// Updates dropdown options
function updateDropdown(dropdownId, options) {
    var dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = ''; // Clears existing options
    // Create and append the 'Select' option
    var defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Select options';
    dropdown.appendChild(defaultOption);
    options.forEach(function(option) {
        var optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        dropdown.appendChild(optionElement);
    });
}


  
  