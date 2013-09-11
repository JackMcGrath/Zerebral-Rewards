//display tooltips on week dots
$("[data-toggle=tooltip]").tooltip();

$("td > span").css('cursor','pointer');

//hover logic for stars
$("tr > td > span").hover(function(evt){
    //onhover

    //calculate the index (from 0) of our current star
    current_star = $(this).siblings().size() - $(this).nextAll().size();

    //remove color from all stars
    $(this).siblings().removeClass('fg-orange');

    //re-add color to stars leading up to the one we're currently hovering
    $(this).siblings().each(function(i,e){
        if(i < current_star) $(e).addClass('fg-darkorange');
    });

    //add it to our current star
    $(this).addClass('fg-darkorange');

},function(evt){
    //hover out
    //return this assessment to its original score
    original_score = $(this).parent().data("score");

    //remove color from all stars
    $(this).parent().children().removeClass('fg-darkorange');

    //re-add color to stars leading up to the one we're currently hovering
    $(this).siblings().each(function(i,e){
        if(i < original_score) $(e).addClass('fg-orange');
    });

});

//click logic for stars
$("tr > td > span").click(function(evt){
    //onclick
    //calculate the new score for the current metric
    new_score = $(this).siblings().size()+1 - $(this).nextAll().size();

    // DO SOMETHING WITH NEW SCORE
    alert("new value "+ new_score);

});

//set colors from initial score
$("tbody > tr > td.evaluations-5star").each(function(index, item){
    score = $(this).data("score");
    $(this).children().each(function(i,e){
        if(i < score) $(e).addClass('text-primary');
    });
});