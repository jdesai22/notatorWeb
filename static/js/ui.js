let currentStatus = 0

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

$(document).ready(function () {
    $("#opts").click(async function () {
        if (currentStatus == 0) {
            console.log("text field viewable")
            await $(".txt").fadeOut();
            await sleep(500)
            await $(".url").fadeIn()
            currentStatus = 1
        } else {
            await $(".url").fadeOut();
            await sleep(500)
            await $(".txt").fadeIn();
            currentStatus = 0
        }

    })
})


