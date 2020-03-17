var varTable;
var role_id;
function LoadTable(sectors, qps, status)
{
    vartable1 = $("#tbl_courses").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": false,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/course_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.course_id = 0;
                d.sectors = sectors;
                d.qps = qps;
                d.status = status;
            },
            error: function (e) {
                $("#tbl_courses tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"visible": (($('#hdn_home_user_role_id').val() =='1')|| ($('#hdn_home_user_role_id').val() =='16'))? true : false,
            //<a onclick="EditCourseDetail(\'' + row.Course_Id + '\',\'' + row.SectorId + '\',\'' + row.QpId + '\')" class="btn" style="cursor:pointer" ><i title="Edit Course" class="fas fa-edit" ></i></a>
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                //if(role_id != 3 && role_id != 8)
                varButtons += '<a onclick="AddSessionCourseDetail('+row.Course_Id+' )" class="btn" style="cursor:pointer" ><i title="Add Session" class="fas fa-plus" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Course_Code" },
            { "data": "Course_Name" },
            { "data": "Qp_Code" },
            { "data": "Qp_Name" },
            { "visible":false,"data": "Practice_Name" },
            {"data": "Is_Active"}
            // { "data": function (row, type, val, meta) {
            //     var varStatus = ""; 
            //     if(row.Is_Active)
            //         varStatus="Active";
            //     else
            //         varStatus="In Active";
            //     return varStatus;
            //     }
            // }
        ],
        
        drawCallback: function(){
            $('#tbl_courses_paginate ul.pagination').addClass("pagination-rounded");
        }


    });
}
function EditCourseDetail(CourseId,SectorId,QpId)
{
    $('#hdn_course_id').val(CourseId);
    $('#form1').submit(); 
    
}
function AddSessionCourseDetail(CourseId){
    $('#hdn_course_id').val(CourseId);
    $('#form1').attr('action', '/assign_course_id_for_session');
    $('#form1').submit();
}

function LoadSectorddl()
{
    var URL=$('#hdn_web_url').val()+ "/All_Sector"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Sectors != null)
                {
                    $('#ddlSector').empty();
                    var count=data.Sectors.length;
                    if( count> 0)
                    {
                        //$('#ddlSector').append(new Option('ALL',''));
                        for(var i=0;i<count;i++)
                            $('#ddlSector').append(new Option(data.Sectors[i].Sector_Name,data.Sectors[i].Sector_Id));
                        
                    }
                    else
                    {
                        $('#ddlSector').append(new Option('ALL',''));
                    }
                    //$("#ddlCenter option[value='0']").attr('disabled','disabled');
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

function LoadQPddl()
{
    var URL=$('#hdn_web_url').val()+ "/AllQPBasedOnSector"
	//alert($('#ddlSector').val().toString())
    $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
		"data": {sector_id : $('#ddlSector').val().toString()},
		success: function (data){
            if(data.QP != null)
                {	
                    $('#ddlQP').empty();
                    var count=data.QP.length;
					//alert(count)
                    if( count> 0)
                    {
                        $('#ddlQP').append(new Option('ALL',''));
                        for(var i=0;i<count;i++)
                            $('#ddlQP').append(new Option(data.QP[i].Qp_Name,data.QP[i].Qp_Id));
                    }
                    else
                    {
                        $('#ddlQP').append(new Option('ALL',''));
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

function LoadTableBasedOnSearch(){
    $("#tbl_courses").dataTable().fnDestroy();
    LoadTable($('#ddlSector').val().toString(),$('#ddlQP').val().toString(),$('#ddlStatus').val()); 
}