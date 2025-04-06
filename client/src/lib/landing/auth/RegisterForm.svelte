<script>
  import InputField from "./InputField.svelte";

  import { notifyAlert, svelteState } from "../../../stores/store.svelte.js";

  let email = $state({
    value: "",
    error: "",
    ariaInvalid: "",
    ariaDescribedby: "email-error",
  });

  let name = $state({
    value: "",
    error: "",
    ariaInvalid: "",
    ariaDescribedby: "name-error",
  });

  let role = $state("student");

  let password = $state({
    value: "",
    error: "",
    ariaInvalid: "",
    ariaDescribedby: "password-error",
  });

  let confirmPassword = $state({
    value: "",
    error: "",
    ariaInvalid: "",
    ariaDescribedby: "confirm-password-error",
  });

  let submitButtonState = $state(true);

  const tryToEnableSubmit = () => {
    return email.ariaInvalid === "false" &&
      password.ariaInvalid === "false" &&
      confirmPassword.ariaInvalid === "false"
      ? false
      : true;
  };

const checkEmailConstraints = async () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email.value.length === 0) {
        email.error = "Email is required";
        email.ariaInvalid = "true";
        submitButtonState = true;
    } else if (!emailRegex.test(email.value)) {
        email.error = "Invalid email format";
        email.ariaInvalid = "true";
        submitButtonState = true;
    } else if (
        !email.value.endsWith("@student.mes.ac.in") &&
        !email.value.endsWith("@mes.ac.in")
    ) {
        email.error = "You are not part of our institution.";
        email.ariaInvalid = "true";
        submitButtonState = true;
    } else {
        email.error = "Looks good!";
        email.ariaInvalid = "false";
        submitButtonState = tryToEnableSubmit();

        // Throttle and assign role based on email domain
        setTimeout(() => {
            if (email.value.endsWith("@student.mes.ac.in")) {
                role = "student";
            } else if (email.value.endsWith("@mes.ac.in")) {
                role = "teacher";
            }
        }, 2000); // Wait for 2 seconds
    }
};

  const checkNameConstraints = () => {
    const nameRegex = /^[a-zA-Z]+(?:\s[a-zA-Z]+)*$/;

    if (name.value.length === 0) {
      name.error = "Name is required";
      name.ariaInvalid = "true";
      submitButtonState = true;
    } else if (!nameRegex.test(name.value)) {
      name.error = "Invalid name format";
      name.ariaInvalid = "true";
      submitButtonState = true;
    } else {
      name.error = "Looks good!";
      name.ariaInvalid = "false";
      submitButtonState = tryToEnableSubmit();
    }
  };

  const checkPasswordConstraints = () => {
    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (password.value.length === 0) {
      password.error = "Password is required";
      password.ariaInvalid = "true";
      submitButtonState = true;
    } else if (!passwordRegex.test(password.value)) {
      password.error =
        "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character";
      password.ariaInvalid = "true";
      submitButtonState = true;
    } else {
      password.error = "Looks good!";
      password.ariaInvalid = "false";
      submitButtonState = tryToEnableSubmit();
    }
  };

  const checkConfirmPasswordConstraints = () => {
    if (confirmPassword.value.length === 0) {
      confirmPassword.error = "Confirm Password is required";
      confirmPassword.ariaInvalid = "true";
      submitButtonState = true;
    } else if (confirmPassword.value !== password.value) {
      confirmPassword.error = "Passwords do not match";
      confirmPassword.ariaInvalid = "true";
      submitButtonState = true;
    } else {
      confirmPassword.error = "Looks good!";
      confirmPassword.ariaInvalid = "false";
      submitButtonState = tryToEnableSubmit();
    }
  };

  const registerUser = async (event) => {
    // Prevent default form submission
    event.preventDefault();

    const formData = {
      email: email.value,
      name: name.value,
      role: role,
      password: password.value,
    };

    try {
      svelteState.loading = true;
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/users`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
            body: JSON.stringify(formData),
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log("User registered successfully:", data);
        svelteState.loading = false;
        notifyAlert("success", "Registration successful! Please log in.");
      } else {
        console.error("Registration failed");
        const errorData = await response.json();
        if (errorData.message) {
          svelteState.loading = false;
          notifyAlert("error", errorData.message);
        } else {
          svelteState.loading = false;
          notifyAlert("error", "An unknown error occurred.");
        }
      }
    } catch (error) {
      svelteState.loading = false;
      console.error("An error occurred while registering:", error);
      notifyAlert("error", "An error occurred while registering.");
    } finally {
      svelteState.loading = false;
    }
  };
</script>

<form>
  <InputField
    id="register-email"
    label="Email"
    type="email"
    bind:value={email.value}
    error={email.error}
    ariaInvalid={email.ariaInvalid}
    ariaDescribedby={email.ariaDescribedby}
    placeholder="Enter your email"
    onInput={checkEmailConstraints}
  />

  <InputField
    id="register-name"
    label="Name"
    type="text"
    bind:value={name.value}
    error={name.error}
    ariaInvalid={name.ariaInvalid}
    ariaDescribedby={name.ariaDescribedby}
    placeholder="Enter your name"
    onInput={checkNameConstraints}
  />

  <InputField
    id="register-password"
    label="Password"
    type="password"
    bind:value={password.value}
    error={password.error}
    ariaInvalid={password.ariaInvalid}
    ariaDescribedby={password.ariaDescribedby}
    placeholder="Enter your password"
    onInput={checkPasswordConstraints}
  />

  <InputField
    id="register-confirm-password"
    label="Confirm Password"
    type="password"
    bind:value={confirmPassword.value}
    error={confirmPassword.error}
    ariaInvalid={confirmPassword.ariaInvalid}
    ariaDescribedby={confirmPassword.ariaDescribedby}
    placeholder="Confirm your password"
    onInput={checkConfirmPasswordConstraints}
  />

  <button
    type="submit"
    class="contrast"
    disabled={submitButtonState}
    onclick={(event) => registerUser(event)}
  >
    <i class="fa-solid fa-user-plus"></i>
    &nbsp; Register
  </button>
</form>
