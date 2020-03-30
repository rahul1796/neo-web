/*
                switch(role_id)
				{
                    case 1:         //Tech Admin
						$('#Home').show();
                        $('#Master_Menu').show();
                        $('#AnchorCenters').show();
                        $('#AnchorCenterType').show();
                        $('#AnchorCenterCategory').show();
                        $('#Org_menu').show();
                        $('#AnchorRoles').show();
                        $('#AnchorUsers').show();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();

                        $('#TMA_content').show();
						$('#TMA_batch_Menu').show();
						$('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
						$('#Mobilization_report_Menu').show();
						$('#Report_Menu').show();
						$('#CoomplianceReport').show();
						//TMA_registraion_Menu, TrainerwiseTMARegistration
						
						$('#Trainer_Menu').show()
						
                        if(goto !="")
                            $("#box").load(goto);
                        break;
                    case 2:         //Mobilizer
						$('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').hide();
						$('#Candidate_Menu').show();
                        
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').hide();
                        $('#Mobilization_report_Menu').hide();
                        $('#Report_Menu').show();
						$('#CoomplianceReport').hide();

						$('#Trainer_Menu').hide();
						
						
						
                        if(goto !=""){
							//candidate_list_page || mcl_report_page
                            if(goto == "candidate_list_page" || goto == "mcl_report_page" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                    case 3:         //Department Head
                        $('#Master_Menu').show();
                        $('#AnchorCenters').show();
                        $('#AnchorCenterType').show();
                        $('#AnchorCenterCategory').show();
                        $('#Org_menu').show();
                        $('#AnchorRoles').show();
                        $('#AnchorUsers').show();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').show();
						$('#CoomplianceReport').hide();
                        if(goto !="")
                            $("#box").load(goto);
                        break;
					case 4:         //Placement Officer
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').hide();
                        
                        $('#TMA_content').hide();
                        $('#TMA_batch_Menu').hide();
                        $('#TMA_report_Menu').hide();
                        $('#MCL_report_Menu').hide();
                        $('#Mobilization_report_Menu').hide();
                        $('#Report_Menu').hide();
						$('#CoomplianceReport').hide();
                        
						$('#Trainer_Menu').hide();
												
                        if(goto !=""){
							// home || batch_list_page || batch_add_edit
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                    case 5:         //Center Manager
						$('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
						$('#CoomplianceReport').hide();
                        
						$('#Trainer_Menu').show();
						
						
                        if(goto != ""){
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "change_password_page" || goto == "trainer_deployment" || goto == "attendance_report" || goto == "batch_sessions" || goto == "mobilization_report" || goto == "registered_candidates_list"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                    case 6:         //Super Admin
                        $('#Master_Menu').show();
                        $('#AnchorCenters').show();
                        $('#AnchorCenterType').show();
                        $('#AnchorCenterCategory').show();
                        $('#Org_menu').show();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').show();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').show();
						$('#CoomplianceReport').hide();
                        if(goto !="")
                            $("#box").load(goto);
                        break;
                    case 7:         //Trainer
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').hide();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').hide();
                        $('#Mobilization_report_Menu').hide();
                        $('#Report_Menu').show();
						$('#CoomplianceReport').hide();
                        
						$('#Trainer_Menu').hide();
						
                        if(goto !=""){
							// home, batch_list_page, batch_add_edit, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit"  || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                    case 8:         //Center Ops
                        $('#Master_Menu').show();
                        $('#AnchorCenters').show();
                        $('#AnchorCenterType').show();
                        $('#AnchorCenterCategory').show();
                        $('#Org_menu').show();
                        $('#AnchorRoles').show();
                        $('#AnchorUsers').show();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').show();
                        if(goto !="")
                            $("#box").load(goto);
                        break;
                    case 9:         //Content Executive
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').hide();
                        if(goto != ""){
                            if(goto == "course_list_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 10:         //Content Executive
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').hide();
                        if(goto != ""){
                            if(goto == "course_list_page" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 11:         //COO
                        $('#Home').show();
                        $('#Master_Menu').show();
                        $('#AnchorCenters').show();
                        $('#AnchorCenterType').show();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
						$('#CoomplianceReport').hide();
                        
                        $('#Trainer_Menu').show();
						
                        if(goto != ""){
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            // if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "change_password_page" || goto == "trainer_deployment" || goto == "attendance_report" || goto == "batch_sessions" || goto == "mobilization_report" || goto == "registered_candidates_list"){
                            //     $("#box").load(goto);
                            // }
                            $("#box").load(goto);
                        }
                        break;
                        case 12:         //P-ops
                        $('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
						$('#CoomplianceReport').hide();
                        
						$('#Trainer_Menu').show();
						
                        if(goto != ""){
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 13:         //Region Manager
                        $('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
                        
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
						$('#CoomplianceReport').hide();
                        
                        $('#Trainer_Menu').show();
						
                        if(goto != ""){
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "change_password_page" || goto == "trainer_deployment" || goto == "attendance_report" || goto == "batch_sessions" || goto == "mobilization_report" || goto == "registered_candidates_list"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 14:         //Cluster Manager
                        $('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
						$('#CoomplianceReport').hide();
                        
                        $('#Trainer_Menu').show();
                        
						
                        if(goto != ""){
                            
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "batch_list_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "change_password_page" || goto == "trainer_deployment" || goto == "attendance_report" || goto == "batch_sessions" || goto == "mobilization_report" || goto == "registered_candidates_list"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 15:         //PMT
                        $('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
                        $('#CoomplianceReport').hide();
						
                        $('#Trainer_Menu').show();
                        
						
                        if(goto != ""){
                            
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "batch_list_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "change_password_page" || goto == "trainer_deployment" || goto == "attendance_report" || goto == "batch_sessions" || goto == "mobilization_report" || goto == "registered_candidates_list"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 16:         //Content
                        $('#Home').hide();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').hide();
						$('#Candidate_Menu').hide();
						
                        $('#TMA_content').hide();
                        $('#TMA_batch_Menu').hide();
                        $('#TMA_report_Menu').hide();
                        $('#MCL_report_Menu').hide();
                        $('#Mobilization_report_Menu').hide();
                        $('#Report_Menu').hide();
                        $('#CoomplianceReport').hide();
						
                        $('#Trainer_Menu').hide();
                        
						
                        if(goto != ""){
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "qp_list_page" || goto == "qp_add_edit" || goto == "course_list_page" || goto == "course_add_edit" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 17:         //PH
                        $('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').show();
                        $('#AnchorCourses').show();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
                        $('#CoomplianceReport').hide();
						
                        $('#Trainer_Menu').show();
						
                        if(goto != ""){
                            
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "batch_list_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "qp_list_page" || goto == "qp_add_edit" || goto == "course_list_page" || goto == "course_add_edit" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 18:         //AUdit Compliance
                        $('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').show();
						$('#Candidate_Menu').show();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
                        $('#CoomplianceReport').show();
						
                        $('#Trainer_Menu').show();
                        
						
                        if(goto != ""){
                            
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "batch_list_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "change_password_page" || goto == "trainer_deployment" || goto == "attendance_report" || goto == "batch_sessions" || goto == "mobilization_report" || goto == "registered_candidates_list" || goto == "trainerwise_tma_registration" || goto == "tma_registration"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                        case 19:         //PH
                        $('#Home').show();
                        $('#Master_Menu').hide();
                        $('#AnchorCenters').hide();
                        $('#AnchorCenterType').hide();
                        $('#AnchorCenterCategory').hide();
                        $('#Org_menu').hide();
                        $('#AnchorRoles').hide();
                        $('#AnchorUsers').hide();
                        $('#Content_Menu').hide();
                        $('#AnchorCourses').hide();
                        $('#Batch_Menu').hide();
						$('#Candidate_Menu').hide();
						
                        $('#TMA_content').show();
                        $('#TMA_batch_Menu').show();
                        $('#TMA_report_Menu').show();
                        $('#MCL_report_Menu').show();
                        $('#Mobilization_report_Menu').show();
                        $('#Report_Menu').show();
                        $('#CoomplianceReport').hide();
						
                        $('#Trainer_Menu').hide();
						
                        if(goto != ""){
                            
							// home, batch_list_page, batch_add_edit, candidate_list_page, trainer_list_page, trainer_add_edit, mcl_report_page, tma_batch_page, tma_report_download_page
                            if(goto == "home" || goto == "batch_list_page" || goto == "batch_add_edit" || goto == "candidate_list_page" || goto == "trainer_list_page" || goto == "trainer_add_edit" || goto == "mcl_report_page" || goto == "tma_batch_page" || goto == "tma_report_download_page" || goto == "batch_list_page" || goto == "mcl_report_page" || goto == "mobilization_report" || goto == "attendance_report" || goto=="trainer_deployment" || goto == "qp_list_page" || goto == "qp_add_edit" || goto == "course_list_page" || goto == "course_add_edit" || goto == "change_password_page"){
                                $("#box").load(goto);
                            }
                        }
                        break;
                }
                */