<script>
  import InputField from "./InputField.svelte";

  import { svelteState } from "../../../stores/store.svelte.js";

  let email = $state({
    value: "",
    error: "",
    ariaInvalid: "",
    ariaDescribedby: "email-error",
  });

  let password = $state({
    value: "",
    error: "",
    ariaInvalid: "",
    ariaDescribedby: "password-error",
  });

  let submitButtonState = $state(true);

  const tryToEnableSubmit = () => {
    return email.ariaInvalid === "false" && password.ariaInvalid === "false"
      ? false
      : true;
  };

  const checkEmailConstraints = () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email.value.length === 0) {
      email.error = "Email is required";
      email.ariaInvalid = "true";
      submitButtonState = true;
    } else if (!emailRegex.test(email.value)) {
      email.error = "Invalid email format";
      email.ariaInvalid = "true";
      submitButtonState = true;
    } else {
      email.error = "Looks good!";
      email.ariaInvalid = "false";
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
        "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter and one number";
      password.ariaInvalid = "true";
      submitButtonState = true;
    } else {
      password.error = "Looks good!";
      password.ariaInvalid = "false";
      submitButtonState = tryToEnableSubmit();
    }
  };

  const getAccessToken = async () => {
    // Prevent default form submission
    event.preventDefault();

    // Check if the form is valid before proceeding
    if (email.ariaInvalid === "true" || password.ariaInvalid === "true") {
      console.error("Form is invalid. Cannot submit.");
      return;
    }

    try {
      svelteState.loading = true;
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/authtoken`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email.value,
            password: password.value,
          }),
          credentials: "include", // Ensure cookies are included in the request
        }
      );

      if (response.ok) {
        console.log("Login successful");
        localStorage.setItem("wasLoggedIn", "true");
        window.location.reload();
      } else {
        const errorData = await response.json();
        console.error("Login failed:", errorData.message);
      }
    } catch (error) {
      console.error("An error occurred while logging in:", error);
    } finally {
      svelteState.loading = false;
    }
  };
</script>

<form>
  <InputField
    id="login-email"
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
    id="login-password"
    label="Password"
    type="password"
    bind:value={password.value}
    error={password.error}
    ariaInvalid={password.ariaInvalid}
    ariaDescribedby={password.ariaDescribedby}
    placeholder="Enter your password"
    onInput={checkPasswordConstraints}
  />

  <button
    type="submit"
    class="contrast"
    disabled={submitButtonState}
    onclick={getAccessToken}
  >
    <i class="fa-solid fa-right-to-bracket"></i>
    &nbsp; Login
  </button>
</form>
