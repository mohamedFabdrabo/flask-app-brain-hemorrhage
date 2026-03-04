/**
 * Brain Hemorrhage Detection UI Script
 * Handles image upload, display, and prediction
 */

$(document).ready(function () {
    'use strict';

    // Hide sections on load
    hideResults();

    /**
     * Handle image file selection and preview
     */
    $("#imageUpload").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function (e) {
                // Display image preview
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').fadeIn(650);
                
                // Show image section with predict button
                $('#image-section').fadeIn(400);
            };
            
            reader.readAsDataURL(this.files[0]);
            
            // Clear previous results
            hideResults();
        }
    });

    /**
     * Handle prediction button click
     */
    $('#btn-predict').click(function () {
        var formData = new FormData($('#upload-file')[0]);

        // Validate file selection
        var fileInput = document.getElementById('imageUpload');
        if (!fileInput.files.length) {
            showError('Please select an image first');
            return;
        }

        // Show loading state
        showLoading(true);

        // Make prediction request
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            timeout: 30000, // 30 second timeout
            success: function (response) {
                showLoading(false);
                
                if (response.success) {
                    displayResults(response);
                } else {
                    showError(response.error || 'Prediction failed');
                }
            },
            error: function (xhr, status, error) {
                showLoading(false);
                
                let errorMsg = 'An error occurred during prediction';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                } else if (status === 'timeout') {
                    errorMsg = 'Request timed out. Please try again.';
                }
                
                showError(errorMsg);
                console.error('Prediction error:', error);
            }
        });
    });

    /**
     * Display prediction results
     */
    function displayResults(response) {
        const prediction = response.prediction;
        const confidence = response.confidence;

        // Set result text and styling
        $('#prediction-text').text(prediction);
        
        const resultCard = $('#result-card');
        resultCard.removeClass('alert-danger alert-success');
        
        // Color code based on prediction
        if (confidence > 50) {
            resultCard.addClass('alert-danger');
        } else {
            resultCard.addClass('alert-success');
        }
        
        $('#confidence-score').text(confidence.toFixed(2));
        
        // Show results container
        $('#results-container').fadeIn(600);
        $('#error-container').hide();
    }

    /**
     * Show error message
     */
    function showError(message) {
        $('#error-message').text(message);
        $('#error-container').fadeIn(400);
        $('#results-container').hide();
    }

    /**
     * Toggle loading animation
     */
    function showLoading(show) {
        if (show) {
            $('#btn-predict').prop('disabled', true);
            $('#loader').fadeIn(300);
        } else {
            $('#btn-predict').prop('disabled', false);
            $('#loader').fadeOut(300);
        }
    }

    /**
     * Hide all result sections
     */
    function hideResults() {
        $('#results-container').hide();
        $('#error-container').hide();
        $('#loader').hide();
    }
});

