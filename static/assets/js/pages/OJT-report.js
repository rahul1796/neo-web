var varTable;


function hideDateStageDiv(){
    $("#alldates").hide();
    
    $("#divBatchStartFromDate").hide();
    $("#divBatchStartToDate").hide();
    $("#divBatchEndFromDate").hide();
    $("#divBatchEndToDate").hide();       
    $("#divOJTStartFromDate").hide();
    $("#divOJTStartToDate").hide();
    $("#divOJTEndFromDate").hide();
    $("#divOJTEndToDate").hide();       
}
function ChangeDateStageDiv(){
    $("#alldates").show();
    //console.log($('#ddlDateStages').val())
    // divBatchFromDate, divBatchToDate, divOJTFromDate, divOJTToDate
    if ($('#ddlDateStages').val()=='1'){
        $("#divBatchStartFromDate").show();
        $("#divBatchStartToDate").show();
        $("#divBatchEndFromDate").show();
        $("#divBatchEndToDate").show();
        $("#divOJTStartFromDate").hide();
        $("#divOJTStartToDate").hide();
        $("#divOJTEndFromDate").hide();
        $("#divOJTEndToDate").hide();   

        $('#OJTStartFromDate').val('');
        $('#OJTStartToDate').val('');
        $('#OJTEndFromDate').val('');
        $('#OJTEndToDate').val('');
    }
    else if ($('#ddlDateStages').val()=='2'){
        $("#divBatchStartFromDate").hide();
        $("#divBatchStartToDate").hide();
        $("#divBatchEndFromDate").hide();
        $("#divBatchEndToDate").hide();
        $("#divOJTStartFromDate").show();
        $("#divOJTStartToDate").show();
        $("#divOJTEndFromDate").show();
        $("#divOJTEndToDate").show();  
        
        $('#BatchStartFromDate').val('');
        $('#BatchStartToDate').val('');
        $('#BatchEndFromDate').val('');
        $('#BatchEndToDate').val('');
    }
    else{
        hideDateStageDiv();
    }
}

function loadClient(){
    var URL=$('#hdn_web_url').val()+ "/GetALLClient"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
        },
        success: function (data){
            if(data.Clients != null)
            {
                $('#ddlClient').empty();
                var count=data.Clients.length;
                if( count> 0)
                {
                    //$('#ddlClient').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlClient').append(new Option(data.Clients[i].Customer_Name,data.Clients[i].Customer_Id));
                }
                else
                {
                    $('#ddlClient').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            //alert($('#ddlClient').val().toString())
            alert('Error! Please try again');
            return false;
        }
    });
}
function loadSubProject(){
    var URL=$('#hdn_web_url').val()+ "/GetsubprojectbyCustomer"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val(),
            "customer_id": $('#ddlClient').val().toString()
        },
        success: function (data){
            if(data.sub_projects != null)
            {
                //console.log(data)
                $('#ddlSubProject').empty();
                var count=data.sub_projects.length;
                if( count> 0)
                {
                    //$('#ddlSubProject').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlSubProject').append(new Option(data.sub_projects[i].Sub_Project_Name,data.sub_projects[i].Sub_Project_Id));
                }
                else
                {
                    $('#ddlSubProject').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            //alert($('#ddlClient').val().toString())
            alert('Error! Please try again');
            return false;
        }
    });
}
function loadCourse(){
    var URL=$('#hdn_web_url').val()+ "/GetCoursesBasedOnSubProjects"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            //"user_id": $('#hdn_home_user_id').val(),
            //"user_role_id": $('#hdn_home_user_role_id').val(),
            "sub_project_ids": $('#ddlSubProject').val().toString()
        },
        success: function (data){
            if(data.Courses != null)
            {
                //console.log(data)
                $('#ddlCourse').empty();
                var count=data.Courses.length;
                if( count> 0)
                {
                    //$('#ddlSubProject').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCourse').append(new Option(data.Courses[i].Course_Name,data.Courses[i].Course_Id));
                }
                else
                {
                    $('#ddlCourse').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            //alert($('#ddlClient').val().toString())
            alert('Error! Please try again');
            return false;
        }
    });
}

function DownloadTableBasedOnSearch(){
    // console.log($('#ddlClient').val().toString() + $('#ddlSubProject').val().toString() + $('#ddlCourse').val().toString())
    // console.log($('#ddlBatches').val() + $('#ddlDateStages').val())
    // console.log($('#BatchFromDate').val() + $('#BatchToDate').val())
    // console.log($('#OJTFromDate').val() + $('#OJTToDate').val())
    
    if ($('#ddlClient').val().toString()=='' && $('#ddlBatches').val()==''){
        alert('please search with customer or batch code');
        return 
    }
    if($('#ddlDateStages').val()=='1'){
        // new Date($('#BatchStartToDate').val()).getTime() > new Date($('#BatchStartFromDate').val()).getTime()
        if ($('#BatchStartFromDate').val()=='' || $('#BatchStartToDate').val() == '' || (new Date($('#BatchStartFromDate').val()).getTime() > new Date($('#BatchStartToDate').val()).getTime())){
            alert('Start date should be less than or equal to End date');
            return
        }
        if ($('#BatchEndFromDate').val()=='' || $('#BatchEndToDate').val() == '' || (new Date($('#BatchEndFromDate').val()).getTime() > new Date($('#BatchEndToDate').val()).getTime())){
            alert('End date should be gearter than or equals to the Start date');
            return
        }
    }
    else if ($('#ddlDateStages').val()=='2'){
        if ($('#OJTStartFromDate').val()=='' || $('#OJTStartToDate').val() == '' || (new Date($('#OJTStartFromDate').val()).getTime() > new Date($('#OJTStartToDate').val()).getTime())){
            alert('Start date should be less than or equal to End date');
            return
        }
        if ($('#OJTEndFromDate').val()=='' || $('#OJTEndToDate').val() == '' || (new Date($('#OJTEndFromDate').val()).getTime() > new Date($('#OJTEndToDate').val()).getTime())){
            alert('End date should be gearter than or equals to the Start date');
            return
        }
    }
    if (1==1){
        $("#imgSpinner").show();
        var URL=$('#hdn_web_url').val()+ "/download_ojt_report"
        $.ajax({
            type: "POST",
            dataType: "json",
            url: URL,
            data: {
                'user_id':$('#hdn_home_user_id').val(),
                'user_role_id':$('#hdn_home_user_role_id').val(),
                'customer_ids':$('#ddlClient').val().toString(),
                'sub_project_ids':$('#ddlSubProject').val().toString(),
                'course_ids':$('#ddlCourse').val().toString(),
                'batch_code':$('#ddlBatches').val(),
                'date_stage':$('#ddlDateStages').val(),

                'BatchStartFromDate':$('#BatchStartFromDate').val(),
                'BatchStartToDate':$('#BatchStartToDate').val(),
                'BatchEndFromDate':$('#BatchEndFromDate').val(),
                'BatchEndToDate':$('#BatchEndToDate').val(),
                
                'OJTStartFromDate':$('#OJTStartFromDate').val(),
                'OJTStartToDate':$('#OJTStartToDate').val(),
                'OJTEndFromDate':$('#OJTEndFromDate').val(),
                'OJTEndToDate':$('#OJTEndToDate').val()
            },
            success: function(resp) 
            {
                //console.log(resp)
                if (resp.Status){
                    var varAnchor = document.getElementById('lnkDownload');
                    varAnchor.href = $('#hdn_web_url').val() + '/report file/' + resp.filename;
                    $("#imgSpinner").hide();
                    try 
                        { 
                            //in firefox
                            varAnchor.click();
                            return;
                        } catch(ex) {}
                        
                        try 
                        { 
                            // in chrome
                            if(document.createEvent) 
                            {
                                var e = document.createEvent('MouseEvents');
                                e.initEvent( 'click', true, true );
                                varAnchor.dispatchEvent(e);
                                return;
                            }
                        } catch(ex) {}
                        
                        try 
                        { 
                            // in IE
                            if(document.createEventObject) 
                            {
                                    var evObj = document.createEventObject();
                                    varAnchor.fireEvent("onclick", evObj);
                                    return;
                            }
                        } catch(ex) {}
                }
                else{
                    alert(resp.Description)
                    $("#imgSpinner").hide();
                    
                }
            },
            error:function()
            {
                //console.log(resp)
                $("#imgSpinner").hide();
            }
        });
    }
    
}

function ForceDownload(varUrl, varFileName)
        {
            var link = document.createElement('a');
            link.setAttribute('href', varUrl);
            link.setAttribute('download', varFileName);
            link.setAttribute('target', '_blank');
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }