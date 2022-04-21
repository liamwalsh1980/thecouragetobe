function sendMail(contactForm) {
    emailjs.send("service_bv0x1rb", "thecouragetobe", {
            "from_name": contactForm.name.value,
            "from_email": contactForm.email.value,
            "contact_number": contactForm.number.value,
            "age": contactForm.age.value,
            "other_information": contactForm.message.value
    })
    .then(
        function (response) {
            console.log("SUCCESS", response);
        },
        function (error) {
            console.log("FAILED", error);
        });
}