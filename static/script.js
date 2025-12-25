/**
 * Badge Counter - Client-Side JavaScript
 * Handles form submission, API calls, and UI updates
 */

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('badgeForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = document.getElementById('spinner');
    const resultContainer = document.getElementById('resultContainer');
    const errorContainer = document.getElementById('errorContainer');
    const badgeCountEl = document.getElementById('badgeCount');
    const errorMessageEl = document.getElementById('errorMessage');
    const profileUrlInput = document.getElementById('profileUrl');

    // Form submission handler
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const profileUrl = profileUrlInput.value.trim();

        // Reset UI
        hideResult();
        hideError();

        // Show loading state
        setLoadingState(true);

        try {
            // Make API request
            const response = await fetch('/count-badges', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    profile_url: profileUrl
                })
            });

            const data = await response.json();

            if (data.success) {
                // Display success result
                displayResult(data.badge_count);
            } else {
                // Display error message
                displayError(data.error || 'An unexpected error occurred');
            }

        } catch (error) {
            // Network or parsing error
            displayError('Failed to connect to the server. Please try again.');
            console.error('Error:', error);
        } finally {
            // Hide loading state
            setLoadingState(false);
        }
    });

    /**
     * Set loading state for the submit button
     */
    function setLoadingState(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            btnText.textContent = 'Counting...';
            spinner.classList.add('active');
        } else {
            submitBtn.disabled = false;
            btnText.textContent = 'Count Badges';
            spinner.classList.remove('active');
        }
    }

    /**
     * Display the badge count result
     */
    function displayResult(count) {
        badgeCountEl.textContent = count;
        resultContainer.classList.remove('hidden');

        // Scroll to result smoothly
        setTimeout(() => {
            resultContainer.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }, 100);

        // Update result message based on count
        const resultMessage = resultContainer.querySelector('.result-message');
        if (count === 0) {
            resultMessage.textContent = 'Start your learning journey today! 🚀';
        } else if (count < 5) {
            resultMessage.textContent = 'Great start! Keep going! 🌟';
        } else if (count < 10) {
            resultMessage.textContent = 'Awesome progress! 🎉';
        } else if (count < 20) {
            resultMessage.textContent = 'You\'re on fire! 🔥';
        } else {
            resultMessage.textContent = 'Incredible achievements! You\'re a star! ⭐';
        }
    }

    /**
     * Display an error message
     */
    function displayError(message) {
        errorMessageEl.textContent = message;
        errorContainer.classList.remove('hidden');

        // Scroll to error smoothly
        setTimeout(() => {
            errorContainer.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }, 100);
    }

    /**
     * Hide the result container
     */
    function hideResult() {
        resultContainer.classList.add('hidden');
    }

    /**
     * Hide the error container
     */
    function hideError() {
        errorContainer.classList.add('hidden');
    }

    /**
     * Add input validation and formatting
     */
    profileUrlInput.addEventListener('blur', function () {
        const url = this.value.trim();
        if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
            // Auto-add https:// if missing
            this.value = 'https://' + url;
        }
    });

    /**
     * Clear errors when user starts typing
     */
    profileUrlInput.addEventListener('input', function () {
        hideError();
    });
});
