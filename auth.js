function getUsers() {
    const usersJSON = localStorage.getItem("users");
    return usersJSON ? JSON.parse(usersJSON) : [];
}

function validatePassword(password) {
    if (!password || password.length < 8) {
        return {
            valid: false,
            message: "Password must be at least 8 characters long"
        };
    }

    if (password.length > 20) {
        return {
            valid: false,
            message: "Password must not exceed 20 characters"
        };
    }

    if (!/[A-Z]/.test(password)) {
        return {
            valid: false,
            message: "Password must contain at least one uppercase letter"
        };
    }

    if (!/[a-z]/.test(password)) {
        return {
            valid: false,
            message: "Password must contain at least one lowercase letter"
        };
    }

    if (!/\d/.test(password)) {
        return {
            valid: false,
            message: "Password must contain at least one number"
        };
    }

    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
        return {
            valid: false,
            message: "Password must contain at least one special character"
        };
    }

    return {
        valid: true,
        message: "Password is valid"
    };
}

function saveUsers(users) {
    localStorage.setItem("users", JSON.stringify(users));
}

function register(name, lastName, phone, password) {
    if (!name || !lastName || !phone || !password) {
        return {
            success: false,
            message: "All fields are required"
        };
    }

    const passwordValidation = validatePassword(password);
    if (!passwordValidation.valid) {
        return {
            success: false,
            message: passwordValidation.message
        };
    }

    const phoneRegex = /^\d{10}$/;
    if (!phoneRegex.test(phone.trim())) {
        return {
            success: false,
            message: "Phone number must be exactly 10 digits"
        };
    }

    const users = getUsers();

    const existingUser = users.find(user => user.phone === phone);
    if (existingUser) {
        return {
            success: false,
            message: "User with this phone number already exists"
        };
    }

    const newUser = {
        name: name.trim(),
        lastName: lastName.trim(),
        phone: phone.trim(),
        password: password.trim()
    };

    users.push(newUser);
    saveUsers(users);

    return {
        success: true,
        message: "Registration successful"
    };
}

function login(phone, password) {
    if (!phone || !password) {
        return {
            success: false,
            message: "All fields are required"
        };
    }

    const users = getUsers();

    const user = users.find(
        u => u.phone === phone.trim() && u.password === password.trim()
    );

    if (!user) {
        return {
            success: false,
            message: "Invalid credentials"
        };
    }

    sessionStorage.setItem("loggedInUser", phone);
    sessionStorage.setItem("userName", user.name);
    sessionStorage.setItem("userLastName", user.lastName);
    sessionStorage.setItem("userType", "user");

    return {
        success: true,
        message: "Login successful",
        user: user
    };
}

function isAuthenticated() {
    return sessionStorage.getItem("loggedInUser") !== null;
}

function getCurrentUser() {
    if (!isAuthenticated()) {
        return null;
    }

    return {
        phone: sessionStorage.getItem("loggedInUser"),
        name: sessionStorage.getItem("userName"),
        lastName: sessionStorage.getItem("userLastName"),
        userType: sessionStorage.getItem("userType")
    };
}

function logout() {
    sessionStorage.removeItem("loggedInUser");
    sessionStorage.removeItem("userName");
    sessionStorage.removeItem("userLastName");
    sessionStorage.removeItem("userType");
}
