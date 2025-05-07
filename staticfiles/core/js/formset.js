document.addEventListener('DOMContentLoaded', function() {
    // Add new job form
    document.getElementById('add-job').addEventListener('click', function() {
        const formsetContainer = document.getElementById('job-formset');
        const totalForms = document.querySelector('#id_form-TOTAL_FORMS');
        const formCount = parseInt(totalForms.value);

        // Clone the first job form as a template
        const template = formsetContainer.querySelector('.job-form').cloneNode(true);
        // Clear the input values and update IDs/names
        template.querySelectorAll('input').forEach(input => {
            if (input.type !== 'hidden' && input.type !== 'checkbox') {
                input.value = ''; // Clear text input
            }
            // Update ID and name to match new form index
            input.id = input.id.replace(/-\d+-/, `-${formCount}-`);
            input.name = input.name.replace(/-\d+-/, `-${formCount}-`);
        });
        // Remove DELETE checkbox if present (not needed for new forms)
        const deleteCheckbox = template.querySelector('input[type="checkbox"]');
        if (deleteCheckbox) {
            deleteCheckbox.remove();
            const label = template.querySelector('label[for="' + deleteCheckbox.id + '"]');
            if (label) label.remove();
        }
        // Append the new form
        formsetContainer.appendChild(template);
        // Update TOTAL_FORMS
        totalForms.value = formCount + 1;
    });

    // Remove job form
    document.getElementById('job-formset').addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-job')) {
            const form = e.target.closest('.job-form');
            const deleteCheckbox = form.querySelector('input[type="checkbox"]');
            if (deleteCheckbox) {
                // For existing jobs, mark for deletion
                deleteCheckbox.checked = true;
                form.style.display = 'none'; // Hide the form
            } else {
                // For new jobs, remove the form entirely
                form.remove();
                // Update TOTAL_FORMS
                const totalForms = document.querySelector('#id_form-TOTAL_FORMS');
                totalForms.value = parseInt(totalForms.value) - 1;
            }
        }
    });
});