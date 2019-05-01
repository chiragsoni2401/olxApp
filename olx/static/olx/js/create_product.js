function validateForm() {

    //Note: to get the form values always use model fields
    var a = document.forms["productForm"]["name"].value;
    var b = document.forms["productForm"]["category"].value;
    var c = document.forms["productForm"]["description"].value;
    var d = document.forms["productForm"]["price"].value;
    var e = document.forms["productForm"]["contact"].value;


    if (a == null || a == "") {
        alert("Please Enter Your Full Name");
        return false;
    } else if (b == null || b == "") {
        alert("Please Select the category");
        return false;
    } else if (c == null || c == "") {
        alert("Please Enter description");
        return false;
    } else if (d == null || d == "" || d < 0) {
        if (d < 0) {
            alert("Price should not be negative");

        }
        else {
            alert("Please Enter Price");

        }
        return false;
    }
    else if (isNaN(e)) {

        alert("Please Enter Your Correct Mobile Number");
        return false;
    }
    else if (e.length != 10) {
        alert("Please Enter Your 10 Digit Mobile Number");
        return false;
    }
    if ($('#gallery tbody').children().length == 0) {
        alert(222);
        return confirm("Do you want to continue without uploading photo?");
    }

}


    // window.onload = function () {
    //     if (typeof history.pushState === "function") {
    //         history.pushState("jibberish", null, null);
    //         window.onpopstate = function () {
    //             history.pushState('newjibberish', null, null);
    //             // Handle the back (or forward) buttons here
    //             window.onbeforeunload = function(){
    //                 alert("Rajesh Kumar");
    //             }
    //             // Will NOT handle refresh, use onbeforeunload for this.
    //         };
    //     }
    //     else {
    //         var ignoreHashChange = true;
    //         window.onhashchange = function () {
    //             if (!ignoreHashChange) {
    //                 ignoreHashChange = true;
    //                 window.location.hash = Math.random();
    //                 // Detect and redirect change here
    //                 // Works in older FF and IE9
    //                 // * it does mess with your hash symbol (anchor?) pound sign
    //                 // delimiter on the end of the URL
    //             }
    //             else {
    //                 ignoreHashChange = false;   
    //             }
    //         };
    //     }
    // }