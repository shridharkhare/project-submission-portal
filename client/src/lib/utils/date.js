const convertDateToHumanReadable = (
    /** @type {string | number | Date} */ dateString
  ) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

export { convertDateToHumanReadable };
