$(document).ready(function () {
          $(".button-collapse").sideNav();
          $(".dropdown-button-laptop-yet").dropdown({
            inDuration: 300,
            outDuration: 225,
            constrainWidth: "auto", // Does not change width of dropdown to that of the activator
            gutter: 0, // Spacing from edge
            belowOrigin: true, // Displays dropdown below the button
            alignment: 'left', // Displays dropdown with edge aligned to the left of button
            stopPropagation: false // Stops event propagation
          });
          $(".dropdown-button-mobile-yet").dropdown({
            inDuration: 300,
            outDuration: 225,
            constrainWidth: "auto", // Does not change width of dropdown to that of the activator
            gutter: 0, // Spacing from edge
            belowOrigin: true, // Displays dropdown below the button
            alignment: 'left', // Displays dropdown with edge aligned to the left of button
            stopPropagation: false // Stops event propagation
          });
          $(".dropdown-button-laptop-support").dropdown({
            inDuration: 300,
            outDuration: 225,
            constrainWidth: "auto", // Does not change width of dropdown to that of the activator
            gutter: 0, // Spacing from edge
            belowOrigin: true, // Displays dropdown below the button
            alignment: 'left', // Displays dropdown with edge aligned to the left of button
            stopPropagation: false // Stops event propagation
          });
          $(".dropdown-button-mobile-support").dropdown({
            inDuration: 300,
            outDuration: 225,
            constrainWidth: "auto", // Does not change width of dropdown to that of the activator
            gutter: 0, // Spacing from edge
            belowOrigin: true, // Displays dropdown below the button
            alignment: 'left', // Displays dropdown with edge aligned to the left of button
            stopPropagation: false // Stops event propagation
          });
        })