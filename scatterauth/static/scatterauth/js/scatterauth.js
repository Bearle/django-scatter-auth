function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loginWithSignature(pubkey, signature, address, login_url, onLoginRequestError, onLoginFail, onLoginSuccess) {
    var request = new XMLHttpRequest();
    request.open('POST', login_url, true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = JSON.parse(request.responseText);
            if (resp.success) {
                if (typeof onLoginSuccess === 'function') {
                    onLoginSuccess(resp);
                }
            } else {
                if (typeof onLoginFail === 'function') {
                    onLoginFail(resp);
                }
            }
        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status);
            if (typeof onLoginRequestError === 'function') {
                onLoginRequestError(request);
            }
        }
    };

    request.onerror = function () {
        console.log("Autologin failed - there was an error");
        if (typeof onLoginRequestError === 'function') {
            onLoginRequestError(request);
        }
        // There was a connection error of some sort
    };
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    var formData = 'pubkey=' + pubkey + '&signature=' + signature + '&address=' + address;
    request.send(formData);
}

function scatterLogin(login_url, onTokenRequestFail, onTokenSignFail, onTokenSignSuccess, // used in this function
                      onLoginRequestError, onLoginFail, onLoginSuccess) {
    // used in loginWithSignature

    // 1. Retrieve arbitrary login token from server
    // 2. Sign it using scatter
    // 3. Send signed message & your eos account name & public key to server
    // 4. If server validates that you signature is valid
    // 4.1 The user with an according eth address is found - you are logged in
    // 4.2 The user with an according eth address is NOT found - you are redirected to signup page


    var request = new XMLHttpRequest();
    request.open('GET', login_url, true);

    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = JSON.parse(request.responseText);
            var token = resp.data;
            console.log("Token: " + token);
            var account = scatter.identity.accounts.find(function (account) {
                return account.blockchain === 'eos'
            });
            scatter.getArbitrarySignature(scatter.identity.publicKey, token).then(result => {
                // Authentication passed, you can also
                // double validate the the public key on their
                // identity has signed the returned `result` which will be
                // your domain
                console.log("Signed message: " + result);
                if (typeof onTokenSignSuccess === 'function') {
                    onTokenSignSuccess(result);
                }
                loginWithSignature(scatter.identity.publicKey, result, account.name,
                    login_url, onLoginRequestError, onLoginFail, onLoginSuccess);

            }).catch(error => {
                if (typeof onTokenSignFail === 'function') {
                    onTokenSignFail(err);
                }
                console.log("Failed signing message \n" + msg + "\n - " + err);
                // Authentication Failed!
            });

        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status);
            if (typeof onTokenRequestFail === 'function') {
                onTokenRequestFail(request);
            }
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
        console.log("Autologin failed - there was an error");
        if (typeof onTokenRequestFail == 'function') {
            onTokenRequestFail(request);
        }
    };
    request.send();
}



