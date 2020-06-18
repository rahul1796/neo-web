var varTable;
var varTable1;
var flag = "";
var role_id;
var check_list = [];

function toggleCheckbox(e)
    {
        //let id = e.target.getAttribute('value');
        
        //console.log(e.target.getAttribute('name'));
        var temp=e.target.getAttribute('value');
        //check_list.push(e.target.getAttribute('value'));

        //console.log(e.target.getAttribute('name').checked)
        //console.log(e.target.getAttribute('name').checked())
        //console.log($('#'+e.target.getAttribute('id')).is(':checked')) 



        //console.log($('#'+e.target.getAttribute('name')).is(':checked'))

        //console.log(e.currentTarget.getAttribute('id'));
        if($('#'+e.target.getAttribute('id')).is(':checked'))
        {
            if(jQuery.inArray( temp, check_list )==-1){
                check_list.push(temp);
            }
        }
        else
        {
            if(jQuery.inArray( temp, check_list )!=-1){
                check_list = $.grep(check_list, function(value) {
                    return value != temp;
                  })
                //check_list = check_list.pop(temp);
            }
        }
        //console.log(check_list)
    }



function UploadFileData()
{   $("#imgSpinner1").show();
    var form_data = new FormData($('#formUpload')[0]);
    form_data.append('cand_stage',3);
    form_data.append('user_id',$('#hdn_home_user_id_modal').val());
    form_data.append('user_role_id',$('#hdn_home_user_role_id_modal').val());
    $.ajax({
            type: 'POST',
            url: $('#hdn_web_url').val()+ "/upload_bulk_upload",
            enctype: 'multipart/form-data',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) 
            {
                var message="",title="",icon="";
                if(data.Status){
                    message=data.message;
                    title="Success";
                    icon="success";
                }
                else{
                    if (data.message=="Validation_Error"){
                        message=data.error;
                        title="Error";
                        icon="error";
                    }
                    else {
                        message=data.message;
                        title="Error";
                        icon="error";
                    }
                }
                var span = document.createElement("span");
                span.innerHTML = message;
                swal({   
                            title:title,
                            content: span,
                            icon:icon,
                            confirmButtonClass:"btn btn-confirm mt-2"
                            }).then(function(){
                                //window.location.href = '/enrollment';
                                $('#mdl_bulkupload_candidate').modal('hide');
                            }); 
            
                    
            },
            error:function(err)
            {
                swal({   
                    title:"Error",
                    text:'Error! Please try again',
                    icon:"error",
                    confirmButtonClass:"btn btn-confirm mt-2"
                    }).then(function(){
                        window.location.href = '/enrollment';
                    }); 
               
            }
        });
    
}
function Uploadfile(){
    $('#hdn_home_user_id_modal').val($('#hdn_home_user_id').val());
    $('#hdn_home_user_role_id_modal').val($('#hdn_home_user_role_id').val());
    $("#imgSpinner1").hide();
    $('#myFile').val('');
    $('#mdl_bulkupload_candidate').modal('show');
}
function Loadcreatedbyddl(){
    var URL=$('#hdn_web_url').val()+ "/AllCreatedByBasedOnUser"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id" : $('#hdn_home_user_role_id').val()
        },

        success: function (data){
            if(data.CreatedBy != null)
            {
                $('#ddlcreated_by').empty();
                var count=data.CreatedBy.length;
                if( count> 0)
                {
                    //$('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlcreated_by').append(new Option(data.CreatedBy[i].User_Name,data.CreatedBy[i].User_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlcreated_by').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading BU! Please try again');
            return false;
        }
    });
    return false;
}
function LoadRegionddl(){
    var URL=$('#hdn_web_url').val()+ "/AllRegionsBasedOnUser"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id" : $('#hdn_home_user_role_id').val(),
            "user_region_id" : $('#hdn_user_region_id').val()
        },

        success: function (data){
            if(data.Regions != null)
            {
                $('#ddlRegion').empty();
                var count=data.Regions.length;
                if( count> 0)
                {
                    //$('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlRegion').append(new Option(data.Regions[i].Region_Name,data.Regions[i].Region_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlRegion').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading BU! Please try again');
            return false;
        }
    });
    return false;
}

function LoadState(){
    var URL=$('#hdn_web_url').val()+ "/all_states_based_on_region"
    $.ajax({
        type:"Get",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            //"CourseId":"",
            "region_id":$('#ddlRegion').val().toString()
        },
        success: function (data){
            if(data.state != null)
            {
                $('#ddlState').empty();
                var count=data.state.length;
                if( count> 0)
                {
                    //$('#ddlCenter').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlState').append(new Option(data.state[i].State_Name,data.state[i].State_Id));
                }
                else
                {
                   // $('#ddlCenter').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {   
            
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}

function LoadTable()
{   //console.log($("#ddlRegion").val().toString(),$("#ddlState").val().toString(),$("#MinAge").val().toString(),$("#MaxAge").val().toString())
    $('#divCandidateList').show();
    vartable = $("#tbl_candidate").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": true,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/enrolled_list_updated",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.candidate_id = 0;
                d.user_id = $('#hdn_home_user_id').val();
                d.user_role_id  = $('#hdn_home_user_role_id').val();
                d.region_ids = $('#ddlRegion').val().toString();
                d.state_ids = $('#ddlState').val().toString();
                d.Pincode = $('#Pincode').val().toString();
                d.created_by  = $('#ddlcreated_by').val().toString();
                d.FromDate  = $('#FromDate').val();
                d.ToDate  = $('#ToDate').val();
            },
            error: function (e) {
                $("#tbl_candidate tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },
        "columns": [
            { "data": "S_No"},
            {
                "data": function (row, type, val, meta) {
                    var varButtons = "";
                    if(row.Is_Check)
                        varButtons += '<input id="addedchk_' + row.S_No + '" name="checkcase" type="checkbox" value="'+row.Candidate_Id+'" onclick="toggleCheckbox(event)">';      
                    return varButtons;
                }
            },
            { "data": "Candidate_Id"},
            { "data": function (row, type, val, meta) {
                varButtons = '<a onclick="CandidateBasicDetails(\'' + row.First_Name + '\',\'' + row.Middle_Name + '\',\'' + row.Last_Name + '\',\'' + row.Salutation + '\',\'' + row.Date_Of_Birth+ '\',\'' + row.Age+ '\',\'' + row.Gender+ '\',\'' + row.Marital_Status+ '\',\'' + row.Caste+ '\',\'' + row.Disability_Status+ '\',\'' + row.Religion + '\')"  style="color:blue;cursor:pointer" >'+row.First_Name+'</a>';
                return varButtons;
                }
            },
            { "data": "Source_Of_Information"},
            {       
                "data": function (row, type, val, meta) {
                    
                    var varButtons='<a onclick="CandidateContactDetails(\'' + row.Primary_Contact_No+ '\',\'' + row.Secondary_Contact_No+ '\',\'' + row.Email_Id+ '\',\'' + row.Present_Address_Line1+ '\',\'' + row.Present_Address_Line2+ '\',\'' + row.Present_Village+ '\',\'' + row.Present_Panchayat+ '\',\'' + row.Present_Taluk_Block+ '\',\'' + row.Present_District+ '\',\'' + row.Present_State_Name+ '\',\'' + row.Present_Pincode+ '\',\'' + row.Present_Country_Name+ '\',\'' + row.Permanent_Address_Line1+ '\',\'' + row.Permanent_Address_Line2+ '\',\'' + row.Permanent_Village+ '\',\'' + row.Permanent_Panchayat+ '\',\'' + row.Permanent_Taluk_Block+ '\',\'' + row.Permanent_District+ '\',\'' + row.Permanent_State_Name+ '\',\'' + row.Permanent_Pincode+ '\',\'' + row.Permanent_Country_Name+ '\')"  style="color:blue;cursor:pointer" >Click Here</a>';
                    return varButtons;
                }
            }
        ],
        drawCallback: function(){
            check_list.forEach(function(value, index){  $('[value='+ value +']').prop('checked',true); });
            $('#tbl_candidate_paginate ul.pagination').addClass("pagination-rounded");
        }
    });
}
function LoadTableBasedOnSearch(){
    //alert($('#ddlRegion').val().toString() + $('#ddlState').val().toString() + $('#MinAge').val() + $('#MaxAge').val())
    $("#tbl_candidate").dataTable().fnDestroy();
    LoadTable(); 
}
function CandidateBasicDetails(FirstName,MiddleName,LastName,Salutation,Dob,Age,gender,MaritalStatus,Caste,Disability,religion)
{
    $('#txtSalutation').val(Salutation);
    $('#txtFirstName').val(FirstName);
    $('#txtMiddleName').val(MiddleName);
    $('#txtLastName').val(LastName);
    $('#txtDob').val(Dob);
    $('#txtAge').val(Age);
    $('#txtgender').val(gender);
    $('#txtMaritalStatus').val(MaritalStatus);
    $('#txtCaste').val(Caste);
    $('#txtDisability').val(Disability);
    $('#txtReligion').val(religion);    
    
    $('#mdl_cand_basic').modal('show');
}
function CandidateContactDetails(primary_contact,SecondaryContact,Email,PresnetAdd1,PresentAdd2,PresentVillage,PresentPanchayat,presentTalukBlock,PresentDist,PresentState,PresentPin,PresentCon,PermanentAdd1,PermanentAdd2,PermanentVillage,PermanentPanchayat,PermanentTalukBlock,PermanentDist,PermanentState,PermanentPin,PermanentCon)
{    
    $('#txtPrCont').val(primary_contact);    
    $('#txtSecondary').val(SecondaryContact); 
    $('#txtEmail').val(Email); 
    $('#txtPrAdd1').val(PresnetAdd1); 
    $('#txtPrAdd2').val(PresentAdd2); 
    $('#txtPrVillage').val(PresentVillage);
    $('#txtPrPanchayat').val(PresentPanchayat);
    $('#txtPrBloack').val(presentTalukBlock);
    $('#txtPrDistrict').val(PresentDist);
    $('#txtPrState').val(PresentState);
    $('#txtPrPin').val(PresentPin);
    $('#txtPrCon').val(PresentCon);
   
    $('#txtPerAdd1').val(PermanentAdd1); 
    $('#txtPerAdd2').val(PermanentAdd2); 
    $('#txtPerVillage').val(PermanentVillage);
    $('#txtPerPanchayat').val(PermanentPanchayat);
    $('#txtPerBloack').val(PermanentTalukBlock);
    $('#txtPerDistrict').val(PermanentDist);
    $('#txtPerState').val(PermanentState);
    $('#txtPerPin').val(PermanentPin);
    $('#txtPerCon').val(PermanentCon);

    $('#mdl_cand_contact').modal('show');
}

function DownloadEnrTemplate(){
    $("#imgSpinner").show();
    var cands=check_list.toString();
    //cands=cands.substring(0,cands.length-1)
    if ((cands.toString().length)==0)
    {
        alert('Please select candidates:')
        $("#imgSpinner").hide();
    }
    else{
        var URL=$('#hdn_web_url').val()+ "/DownloadEnrTemplate"
        //window.location = URL + "?ActivityDate=2019-09-09"
        $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: URL, 
                    data: {
                            //candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
                            
                            'user_id':$('#hdn_home_user_id').val(),
                            'user_role_id':$('#hdn_home_user_role_id').val(),
                            'candidate_ids':cands.toString()
                    },
                    success: function(resp) 
                    {

                        if (resp.Status){
                            var varAnchor = document.getElementById('lnkDownload');
                            varAnchor.href = $('#hdn_web_url').val() + '/Bulk Upload/' + resp.filename;
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
                            //alert(resp.Description)
                            //alert('Not success')
                            $("#imgSpinner").hide();
                            
                        }
                    },
                    error:function()
                    {
                        //$("#imgSpinner").hide();
                    }
                });
        
    }
    //$("#imgSpinner").hide();
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