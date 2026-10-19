document.addEventListener(
    "DOMContentLoaded",
    function () {

        const timer =
            document.getElementById("timer");

        if (timer) {

            let time = 60;

            const interval =
                setInterval(function () {

                    time--;

                    timer.innerText = time;

                    if (time <= 0) {

                        clearInterval(interval);

                        const form =
                            document.querySelector(
                                ".quiz-card form"
                            );

                        if (form) {
                            form.submit();
                        }

                    }

                }, 1000);
        }

    }
);