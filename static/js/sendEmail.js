// function sendMail(contactForm) {
//     emailjs.send("service_bv0x1rb", "thecouragetobe", {
//             "from_name": contactForm.name.value,
//             "from_email": contactForm.email.value,
//             "contact_number": contactForm.number.value,
//             "age": contactForm.age.value,
//             "other_information": contactForm.message.value
//     })
//     .then(
//         function (response) {
//             console.log("SUCCESS", response);
//         },
//         function (error) {
//             console.log("FAILED", error);
//         });
// }

function sendMail(contactForm) {
    var modal = document.getElementById("modal");

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
            $(".modal-message").text("Thank you for taking the first step " + contactForm.name.value + ". I'll be in touch very soon, Brian");
            modal.style.display = "block";
            $("#closing-btn").click(function () {
                location.reload();
            });
        },
        function (error) {
            console.log("FAILED", error);
            $(".modal-message").text("Sorry " + contactForm.name.value + " something went wrong. Please try submitting your feedback again!");
            modal.style.display = "block";
            $("#closing-btn").click(function () {
                location.reload();
            });
        });
    return false;
}