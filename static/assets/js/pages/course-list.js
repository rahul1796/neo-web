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
                d.user_id =$('#hdn_home_user_id').val();
                d.user_role_id = $('#hdn_home_user_role_id').val();
            },
            error: function (e) {
                $("#tbl_courses tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"visible": (($('#hdn_home_user_role_id').val() =='1')|| ($('#hdn_home_user_role_id').val() =='16'))? true : false,
            //<a onclick="EditCourseDetail(\'' + row.Course_Id + '\',\'' + row.SectorId + '\',\'' + row.QpId + '\')" class="btn" style="cursor:pointer" ><i title="Edit Course" class="fas fa-edit" ></i></a>
            "orderable":false,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                //if(role_id != 3 && role_id != 8)
                varButtons += '<a onclick="AddSessionCourseDetail('+row.Course_Id+' )" class="btn" style="cursor:pointer" ><i title="Add Session" class="fas fa-plus" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Course_Code" },
            { "data": "Course_Name" },
              { //"orderable":false,
              "data": 
              function (row, type, val, meta) {
                  var varButtons = ""; 
                  if(row.Course_Variant_Count==0)
                      varButtons=row.Course_Variant_Count;
                  else
                  {
                      varButtons += '<a onclick="Get_Course_Variants(\'' + row.Course_Id + '\',\'' + row.Course_Name + '\')"  style="color:blue;cursor:pointer" >' + row.Course_Variant_Count + '</a>';
                  }                    
                  return varButtons;
              }
          },
            { //"orderable":false,
                "data": 
                function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Project_Count==0)
                        varButtons=row.Project_Count;
                    else
                    {
                        varButtons += '<a onclick="Get_projects(\'' + row.Course_Id + '\',\'' + row.Course_Name + '\',0)"  style="color:blue;cursor:pointer" >' + row.Project_Count + '</a>';
                    }                    
                    return varButtons;
                }
            },
            { //"orderable":false,
                "data": 
                function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Sub_Project_Count==0)
                        varButtons=row.Sub_Project_Count;
                    else
                    {
                        varButtons += '<a onclick="Get_Sub_Projects(\'' + row.Course_Id + '\',\'' + row.Course_Name + '\',0)"  style="color:blue;cursor:pointer" >' + row.Sub_Project_Count + '</a>';
                    }                    
                    return varButtons;
                }
            },
            { //"orderable":false,
                "data": 
                function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(row.Center_Count==0)
                        varButtons=row.Center_Count;
                    else
                    {
                        varButtons += '<a onclick="Get_Centers(\'' + row.Course_Id + '\',\'' + row.Course_Name + '\',0)"  style="color:blue;cursor:pointer" >' + row.Center_Count + '</a>';
                    }                    
                    return varButtons;
                }
            },
            { "data": "Qp_Code" },
            { "data": "Qp_Name" },
            {"data": "Is_Active"}
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

function getmodal(a){
    $('#mdl_cand_identity').modal('show');
    alert(a);
}
function Get_projects(CourseId,CourseName,IsCourseVariant){
    $('#hdn_is_course_variant').val(IsCourseVariant);
    if(IsCourseVariant==1) 
        $('#mdl_Cou_variants').modal('hide');
   $('#hdCourseName').text('Projects of '+ CourseName);
    var URL=$('#hdn_web_url').val()+ "/GetProjectsForCourse?CourseId="+CourseId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tbl_project").dataTable().fnDestroy();
            $("#tbl_project tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   
                if (data.Projects != null){
                    var count=data.Projects.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                        {
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.Projects[i].S_No +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Project_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Project_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Contract_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Contract_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Customer_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Customer_Code +'</td>';
                            varHtml+='</tr>';
                        }                        
                    }
                    $("#tbl_project tbody").append(varHtml);
                    $("#tbl_project").DataTable();
                    $('#mdl_Cou_Projects').modal('show');
                }
                else
                {
                    varHtml='<tr><td colspan="7" style="text-align:center;">No records found</td></tr>'
                    $("#tbl_project tbody").append(varHtml);
                    $('#mdl_Cou_Projects').modal('show');
                }
            }
            else
            {
                varHtml='<tr><td colspan="7" style="text-align:center;">No records found</td></tr>'
                $("#tbl_project tbody").append(varHtml);
                $('#mdl_Cou_Projects').modal('show');
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

function Get_Sub_Projects(CourseId,CourseName,IsCourseVariant){
    $('#hdn_is_course_variant').val(IsCourseVariant);
    
    if(IsCourseVariant==1) 
        $('#mdl_Cou_variants').modal('hide');
    $('#headerName').text('Sub Projects of '+CourseName);
     var URL=$('#hdn_web_url').val()+ "/GetSubProjectsForCourse?CourseId="+CourseId;
     $.ajax({
         type:"GET",
         url:URL,
         async:false,
         overflow:true,        
         beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
         datatype:"json",
         success: function (data){
             varHtml='';
             $("#tbl_sub_project").dataTable().fnDestroy();
             $("#tbl_sub_project tbody").empty();
             if(!jQuery.isEmptyObject(data))
             {   
                 if (data.Projects != null){
                     var count=data.Projects.length;
                     if( count> 0)
                     {
                         for(var i=0;i<count;i++)
                         {
                             varHtml+='<tr>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].S_No +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Sub_Project_Name +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Sub_Project_Code +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Project_Name +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Project_Code +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Contract_Name +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Contract_Code +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Customer_Name +'</td>';
                             varHtml+='  <td style="text-align:center;">'+ data.Projects[i].Customer_Code +'</td>';
                             varHtml+='</tr>';
                         }                        
                     }
                     $("#tbl_sub_project tbody").append(varHtml);
                     $("#tbl_sub_project").DataTable();
                     $('#mdl_Cou_Sub_Projects').modal('show');
                 }
                 else
                 {
                     varHtml='<tr><td colspan="9" style="text-align:center;">No records found</td></tr>'
                     $("#tbl_sub_project tbody").append(varHtml);
                     $('#mdl_Cou_Sub_Projects').modal('show');
                 }
             }
             else
             {
                 varHtml='<tr><td colspan="9" style="text-align:center;">No records found</td></tr>'
                 $("#tbl_sub_project tbody").append(varHtml);
                 $('#mdl_Cou_Sub_Projects').modal('show');
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
 
 function Get_Centers(CourseId,CourseName,IsCourseVariant)
 {
    $('#hdn_is_course_variant').val(IsCourseVariant);
    if(IsCourseVariant==1) 
        $('#mdl_Cou_variants').modal('hide');
    $('#headerCenter').text(CourseName);
    var URL=$('#hdn_web_url').val()+ "/GetCentersForCourse?CourseId="+CourseId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            let varTxt='';
            $("#tbl_centers").dataTable().fnDestroy();
            $("#tbl_centers tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   
                if (data.Centers != null){
                    var count=data.Centers.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                        {
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].S_No +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Center_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Center_Code +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Center_Type_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].State_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.Centers[i].Region_Name +'</td>';
                            varHtml+='</tr>';
                        }                        
                    }
                    $("#tbl_centers tbody").append(varHtml);
                    $("#tbl_centers").DataTable();
                    $('#mdl_Cou_Centes').modal('show');
                }
                else
                {
                    varHtml='<tr><td colspan="6" style="text-align:center;">No records found</td></tr>'
                    $("#tbl_centers tbody").append(varHtml);
                    $('#mdl_Cou_Centes').modal('show');
                }
            }
            else
            {
                varHtml='<tr><td colspan="6" style="text-align:center;">No records found</td></tr>'
                $("#tbl_centers tbody").append(varHtml);
                $('#mdl_Cou_Centes').modal('show');
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

 function Get_Course_Variants(CourseId,CourseName)
 {
    $('#headerNameCouVariants').text('Variants of '+CourseName);
    var URL=$('#hdn_web_url').val()+ "/GetCourseVariantsForCourse?CourseId="+CourseId;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            let varTxt='';
            $("#tbl_course_variants tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   
                if (data.CourseVariants != null){
                    var count=data.CourseVariants.length;
                    if( count> 0)
                    {
                        for(var i=0;i<count;i++)
                        {
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.CourseVariants[i].S_No +'</td>';
                            varTxt= '<a onclick="AddSessionCourseDetail('+data.CourseVariants[i].Course_Id+' )" class="btn" style="cursor:pointer" ><i title="Add Session" class="fas fa-plus" ></i></a>';
                            varHtml+='  <td style="text-align:center;">'+ varTxt +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.CourseVariants[i].Course_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.CourseVariants[i].Course_Code +'</td>';
                            if(data.CourseVariants[i].Project_Count==0)
                                varTxt=data.CourseVariants[i].Project_Count;
                            else
                                varTxt= '<a onclick="Get_projects(\'' + data.CourseVariants[i].Course_Id  + '\',\'' + data.CourseVariants[i].Course_Name + '\',1)"  style="color:blue;cursor:pointer" >' + data.CourseVariants[i].Project_Count + '</a>';
                            varHtml+='  <td style="text-align:center;">'+ varTxt +'</td>';
                            if(data.CourseVariants[i].Sub_Project_Count==0)
                                varTxt=data.CourseVariants[i].Sub_Project_Count;
                            else
                                varTxt='<a onclick="Get_Sub_Projects(\'' + data.CourseVariants[i].Course_Id + '\',\'' + data.CourseVariants[i].Course_Name + '\',1)"  style="color:blue;cursor:pointer" >' + data.CourseVariants[i].Sub_Project_Count + '</a>';
                            varHtml+='  <td style="text-align:center;">'+ varTxt +'</td>';
                            
                            if(data.CourseVariants[i].Center_Count==0)
                                varTxt=data.CourseVariants[i].Center_Count;
                            else
                                varTxt='<a onclick="Get_Centers(\'' + data.CourseVariants[i].Course_Id + '\',\'' + data.CourseVariants[i].Course_Name + '\',1)"  style="color:blue;cursor:pointer" >' + data.CourseVariants[i].Center_Count + '</a>';
                            varHtml+='  <td style="text-align:center;">'+ varTxt +'</td>';
                            
                            varHtml+='</tr>';

                        }                        
                    }
                    $("#tbl_course_variants tbody").append(varHtml);
                    $('#mdl_Cou_variants').modal('show');
                }
                else
                {
                    varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                    $("#tbl_course_variants tbody").append(varHtml);
                    $('#mdl_Cou_variants').modal('show');
                }
            }
            else
            {
                varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                $("#tbl_course_variants tbody").append(varHtml);
                $('#mdl_Cou_variants').modal('show');
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
 function OpenCourseVariantModal(){
     if($('#hdn_is_course_variant').val()=='1')
        $('#mdl_Cou_variants').modal('show');
 }