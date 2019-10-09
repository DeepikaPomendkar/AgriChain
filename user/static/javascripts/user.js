$(document).ready(function(){
    var myOptions1 = [];
    $.ajax({
            type: "GET",
            url: "getData/",
            data: {
				'requestData':'yieldIds'
            },
            success: function (data) {
//                alert(data);
                $.each( data, function( key, value ) {
                    myOptions1[key] = value;
                });
                console.log(myOptions1)
                var mySelect1 = $('#idSelect');
                 $.each(myOptions1, function(key,value) {
//                    console.log(value.yieldIds)
                    mySelect1.append( $('<option></option>').val(value.yieldIds).html(value.yieldIds));
                });
            }
     });
     $('#idSelect').on('change',function () {
            var selectedItem = $(this).val();
//	        alert('hey');
            var myOptions = []
            $.ajax({
                type: "GET",
                url: "getData/",
                data: {
                    'requestData':'lotIds',
                    'selectedItem': selectedItem,
                },
                success: function (data) {
    //                alert(data);
                    $.each( data, function( key, value ) {
                        myOptions[key] = value;
                    });
                    console.log(myOptions);
                    var mySelect = $('#lotIdSelect');
                     $.each(myOptions, function(key,value) {
//                        console.log(value)
                        mySelect.append( $('<option></option>').val(value.lotNumbers).html(value.lotNumbers));
                    });
                }
            });
     });
     $('#lotIdSelect').on('change',function(){
//        alert('hey');
//        alert();
        document.getElementById("lotIdSelected").value = document.getElementById('lotIdSelect').value;
        document.getElementById("idSelected").value = document.getElementById('idSelect').value;
     });
});