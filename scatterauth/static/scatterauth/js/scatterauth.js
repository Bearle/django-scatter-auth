function jtrim(text) {
    var rtrim = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;
    return text == null ?
        "" :
        (text + "").replace(rtrim, "");
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jtrim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loginWithAuthenticate(login_url, onSignatureFail, onSignatureSuccess,
                               onLoginRequestError, onLoginFail, onLoginSuccess) {
    scatter.authenticate().then(signature => {
        if (typeof onSignatureSuccess === 'function') {
            onSignatureSuccess(signature);
        }
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
                console.log("Scatter login failed - request status " + request.status);
                if (typeof onLoginRequestError === 'function') {
                    onLoginRequestError(request);
                }
            }
        };

        request.onerror = function () {
            console.log("Scatter login failed - there was an error");
            if (typeof onLoginRequestError === 'function') {
                onLoginRequestError(request);
            }
            // There was a connection error of some sort
        };
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        var formData = 'pubkey=' + scatter.identity.publicKey + '&signature=' + signature;
        request.send(formData);

    }).catch(signatureError => {
        if (typeof onSignatureFail === 'function') {
            onSignatureFail(signatureError);
        }
    })
}


function signupWithData(pubkey, pubkeyFieldName, email, signup_url, onSignupRequestError, onSignupSuccess, onSignupFail) {
    var request = new XMLHttpRequest();
    request.open('POST', signup_url, true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = JSON.parse(request.responseText);
            if (resp.success) {
                if (typeof onSignupSuccess === 'function') {
                    onSignupSuccess(resp);
                }
            } else {
                if (typeof onSignupFail === 'function') {
                    onSignupFail(resp);
                }
            }
        } else {
            // We reached our target server, but it returned an error
            console.log("Signup failed - request status " + request.status);
            if (typeof onSignupRequestError === 'function') {
                onSignupRequestError(request);
            }
        }
    };

    request.onerror = function () {
        console.log("Signup failed - there was an error");
        if (typeof onSignupRequestError === 'function') {
            onSignupRequestError(request);
        }
        // There was a connection error of some sort
    };
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    var formData = pubkeyFieldName + '=' + pubkey + '&email=' + email;
    request.send(formData);
}

async function requestIdentity(requiredFields, pubkeyFieldName, signup_url, network, onIdentityReject) {
    let identitySettings = {
        personal: requiredFields,
    };
    if (network) {
        await scatter.suggestNetwork(network);
        identitySettings['accounts'] = network;
    }

    scatter.getIdentity(identitySettings).then((identity) => {
        signupWithData(identity.publicKey, pubkeyFieldName, identity.personal.email, signup_url, console.log, console.log, console.log)
    }).catch(error => {
        console.log("Identity or Network was rejected");
        if (typeof onIdentityReject === 'function') {
            onIdentityReject(error);
        }
    })
}
