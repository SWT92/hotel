$(document).ready(function() {
    // When there is a change in #passport
    $("#passport").on('change', function() {
        $(".alert-box").empty();
        $(".alert-box").hide();
        // Check if #passport has a value
        if ($(this).val()) {
            $('#list-tab').empty();
            $('#list-tab').append('<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>');
            let passport = { passport: $(this).val() };

            // Send a POST request using $.ajax
            $.ajax({
                type: "POST",
                url: "/getCheckInBookings",
                data: JSON.stringify(passport),
                contentType: "application/json",
                success: function(response) {
                    $('#list-tab').empty();

                    console.log(response);

                    let listtab_Output = '';
                    let tabContent_Output = '';
                    
                    for (const item of response) {
                        const checkInDate = item.checkInDate;
                        const checkOutDate = item.checkOutDate;
                        const room = item.roomType;
                        const bed = item.bedType;
                        const status = item.status;
                        const totalCost = item.totalCost;
                        listtab_Output += `<a class="list-group-item list-group-item-action" id="${checkInDate}" data-bs-toggle="tab" href="#list-${checkInDate}" role="tab" aria-controls="list-${checkInDate}">${checkInDate}</a>`;
                        tabContent_Output += `<div class="tab-pane fade" id="list-${checkInDate}" role="tabpanel" aria-labelledby="${checkInDate}">`;
                        tabContent_Output += `<h2> Booking Details :</h2>`;
                        tabContent_Output += `<p id="checkInDate">Check In : ${checkInDate}</p>`;
                        tabContent_Output += `<p>Check Out : ${checkOutDate}</p>`;
                        tabContent_Output += `<p>Room : ${room}</p>`;
                        tabContent_Output += `<p>Bed : ${bed}</p>`;
                        if (item.amenities.length > 0) {
                            tabContent_Output += `<p>Amenities : </p>`;
                            tabContent_Output += `<ol>`;
                            for (const amenity of item.amenities) {
                                tabContent_Output += `<li> ${amenity.description}</li>`;
                            }
                            tabContent_Output += `</ol>`;
                        }
                        else {
                            tabContent_Output += `<p>Amenities : None</p>`;
                        }
                        tabContent_Output += `<p>Status : ${status}</p>`;
                        tabContent_Output += `<p>Total Cost : $${totalCost}</p>`;
                        if (status != "Checked In") {
                            tabContent_Output += `<button class="btn btn-primary btn-sm float-end checkInButton">Check In</button>`;
                        }
                        tabContent_Output += '</div>';
                    }
                    $('#list-tab').empty();
                    $('#list-tab').append(listtab_Output);
                    $('#nav-tabContent').empty();
                    $('#nav-tabContent').append(tabContent_Output);

                    $('.checkInButton').click(function() {
                        let fullCheckInText = $(this).closest('.tab-pane').find('p#checkInDate').text();
                        let checkInDate = fullCheckInText.split(' : ')[1].trim();
                        let data = {
                            "checkInDate": checkInDate,
                            "passport": passport.passport
                        };
                        console.log(data);
                        $.ajax({
                            type: "POST",
                            url: "/updateCheckInBookings",
                            data: JSON.stringify(data),
                            contentType: "application/json",
                            success: function(response) {
                                $(".alert-box").text(passport.passport+" checked in on "+ checkInDate);
                                $(".alert-box").show();

                                $("#passport").val('');
                                $('#list-tab').empty();
                                $('#nav-tabContent').empty();
                            },
                            error: function(error){
                                console.log("Error : ", error)
                            }
                        });
                    });
                },
                error: function(error) {
                    // Handle any errors that occur during the request
                    console.log('Error:', error);
                }
            });
        }
    });
});
