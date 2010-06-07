jQuery(document).ready(function($) {
    // new task
    $('#newtask').submit(function() {
        var e = $(this);
        $.ajax({
            type   : 'POST',
            url    : '/new/{{ list.owner.user_id }}',
            data   : e.serialize(),
            success: function(data,msg,xhr) { console.log(data); }
        });
        return false;
    });
    // inline editing!
    $('.task li').dblclick(function() {
        var elm = $(this);
        var cls = elm.attr('class');
        var htm = elm.html();
        var txt = elm.text();
        var key = elm.parent().attr('id');
        elm.html('<form name="task" action="" method="post"><input class="inline" name="'+cls+'" type="text" value="'+txt+'"><input type="hidden" name="key" value="'+key+'"></form>');
        // Attach handler manually, since form is added after jQuery binds its triggers /via @lzimm
        elm.children("form").submit(function() {
        	var e = $(this);
	        $.ajax({
	            type   : 'POST',
	            url    : '/edit/{{ list.owner.user_id }}',
	            data   : e.serialize(),
	            success: function(data,msg,xhr) { console.log(data); e.text(data); }
	        });
	        return false;
        });
        elm.children().children().focus();
        elm.children().children().blur(function() { elm.html(txt); });
    });

    $('form').submit(function() {
		var e = $(this);
        console.log(e.serialize());
        $.ajax({
            type    : 'POST',
            url     : '/u/{{ list.owner.user_id }}',
            data    : e.serialize(),
            success : function(data,msg,xhr) {
                if (data) { e.append('<small style="display:none;color:#3a3;">'+data+'<small>'); }
                else { e.append('<small style="display:none;color:#f33;">Failed.<small>'); }
                e.children('small').fadeIn(50).delay(1000).fadeOut(500);
            }
        });
        e.children('small').remove();
        return false;
    });
    
    // sort that shit
    $("#sortable").sortable({
    	start: function(event,ui) { $(ui.item).addClass('active'); },
        stop : function(event,ui) {
        	$(ui.item).removeClass('active');
            var sortkeys = [];
            $("#sortable .item").each(function(i) { sortkeys.push($(this).attr('id')); });
            $.ajax({
                type    : 'POST',
                url     : '/edit/{{ list.owner.user_id }}',
                data    : { priority: sortkeys },
                success : function(data,msg,xhr) { console.log(data); }
            });
        }
    });
    $("#sortable").disableSelection();
    
    // let em know!
    $("#loading").ajaxStart(function(){ $(this).fadeIn(0); });
    $("#loading").ajaxStop(function(){ $(this).fadeOut(500); });
});