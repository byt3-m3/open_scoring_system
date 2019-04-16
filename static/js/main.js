function makeLeaderboard() {
    $.ajax({
        "url": "/api/v1/leaderboard",
        data: {},
        method: 'GET',
        statusCode: {
            200: function (response) {
                let teams = response.data;

                $('#TEAM_LIST').empty()

                teams.forEach(function (element) {
                    if (element.name != "ringmaster") {
                        if (element.alias) {
                            $('#TEAM_LIST').append(`<li class="MontserratBlack list-group-item">${element.name.toUpperCase()} - ${element.points} pts</li>`);
                        } else {
                            $('#TEAM_LIST').append(`<li class="MontserratBlack list-group-item">${element.name.toUpperCase()} - ${element.points} pts</li>`);
                        }

                    }


                })


            },

            400: function (response) {

            },

            404: function (response) {

            }
        }
    })


}

function popup(mylink, windowname) {
    if (!window.focus) return true;
    var href;
    if (typeof (mylink) == 'string') href = mylink; else href = mylink.href;
    window.open(href, windowname, 'width=600,height=800,scrollbars=yes');
    return false;
}

function updateTeamPoints() {

    $.ajax({
        "url": "/api/v1/teams",
        data: {}, //Insert FormData feilds here.
        method: 'GET',
        statusCode: {
            200: function (response) {
                let docs = response.data

                docs.forEach(function (doc) {
                    $(`#${doc.name}`).attr("placeholder", `${doc.points} POINTS`).val("");

                    
                })


            },
            201: function (response) {

            },

            400: function (response) {

            },
            404: function (response) {

            },

            417: function (response) {

            },
            500: function (response) {

            }
        }
    })

}


