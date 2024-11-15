// Helper function to get CSRF token from cookies
    /*function getCsrfToken() {
        let name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to fetch the link token from the backend  -- Rahul
    async function linkTokenFunc() {

        console.log("Maisha ALOMMMMMMMMMM")
        try {

            // Fetch the link token from the backend endpoint
            const response = await fetch('/create_link_token/');
            if (!response.ok) {
                throw new Error('Failed to fetch link token');
            }
            const data = await response.json();
            return data.link_token;  // Assuming your backend returns the token in `link_token` key
        } catch (error) {
            console.log("Maisha ALOMMMMMMMMMM Returns")
            console.error('Error fetching link token:', error);
            return null;
        }
    }

    // Function to initialize Plaid Link
    async function initializePlaidLink() {
        const linkToken = await linkTokenFunc();
        if (!linkToken) {
            console.error('Link token is null. Cannot initialize Plaid Link.');
            document.getElementById('message').innerHTML = `<p style="color: red;">Error: Could not generate link token. Please try again later.</p>`;
            return;
        }

        // Initialize Plaid Link with the retrieved link token
        var linkHandler = Plaid.create({
            token: linkToken,
            onSuccess: function(public_token, metadata) {
                // Send the public_token to your server to exchange it for an access token
                fetch('/exchange_public_token/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify({ public_token: public_token })
                }).then(response => response.json())
                .then(data => {
                    console.log('Server Response:', data);
                    // Handle success, like navigating the user to the next part of your app
                    document.getElementById('message').innerHTML = `<p style="color: green;">Success: Your bank account has been linked!</p>`;
                })
                .catch(error => {
                    console.error('Error in exchanging public token:', error);
                    document.getElementById('message').innerHTML = `<p style="color: red;">Error: Could not exchange token. Please try again.</p>`;
                });
            },
            onExit: function(err, metadata) {
                // Handle the case when a user exits Link
                if (err != null) {
                    console.error('User exited Plaid Link:', err);
                    document.getElementById('message').innerHTML = `<p style="color: red;">Error: User exited the link process. Please try again.</p>`;
                }
            }
        });

        // Open Plaid Link when button is clicked
        document.getElementById('link-button').onclick = function() {

            console.log("Check if its called")
            linkHandler.open();
        };
    }

    // Initialize Plaid Link when the DOM is fully loaded
    document.addEventListener("DOMContentLoaded", initializePlaidLink);*/

