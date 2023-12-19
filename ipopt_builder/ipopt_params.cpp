#include "ipopt_params.h"

void set_all_default_settings(SmartPtr<IpoptApplication> *app) {
    (*app)->Options()->SetNumericValue("acceptable_tol",  1e-09); //"Acceptable" convergence tolerance(relative).(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("accept_after_max_steps", -1); // Accept a trial point after maximal this number of steps.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("accept_every_trial_step", "no"); //Always accept the first trial step.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("acceptable_compl_inf_tol",  0.01); //"Acceptance" threshold for the complementarity conditions.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("acceptable_constr_viol_tol",  0.01); //"Acceptance" threshold for the constraint violation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("acceptable_dual_inf_tol",  10000000000.0); //"Acceptance" threshold for the dual infeasibility.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("acceptable_iter",  15); //Number of "acceptable" iterates before triggering termination.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("acceptable_obj_change_tol",  1e+20); //"Acceptance" stopping criterion based on objective function change.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("acceptable_tol",  1e-06); //"Acceptable" convergence tolerance(relative).(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("adaptive_mu_kkterror_red_fact",  0.9999); //Sufficient decrease factor for "kkt-error" globalization strategy.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("adaptive_mu_kkterror_red_iters",  4); //Maximum number of iterations requiring sufficient progress.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("adaptive_mu_monotone_init_factor",  0.8); //Determines //the initial value of the barrier parameter when switching to the monotone mode.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("adaptive_mu_restore_previous_iterate",  "no"); //Indicates //if the previous iterate should be restored if the monotone mode is entered.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("adaptive_mu_safeguard_factor",  0.0); //(see IPOPT //documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("alpha_for_y",  "primal"); //Method to determine the step size for constraint multipliers.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("alpha_for_y_tol",  10.0); //Tolerance for switching to full equality multiplier steps.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("alpha_min_frac",  0.05); //Safety factor for the minimal step size(before switching to restoration phase).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("alpha_red_factor",  0.5); //Fractional //reduction of the trial step size in the backtracking line search.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("barrier_tol_factor",  10.0); //Factor for mu in barrier stop test.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("bound_frac",  0.01); //Desired minimum relative distance from the initial point to bound.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("bound_mult_init_val",  1.0); //Initial value for the bound multipliers.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("bound_mult_reset_threshold",  1000.0); //Threshold for resetting bound multipliers after the restoration phase.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("bound_push",  0.01); //Desired minimum absolute distance from the initial point to bound.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("bound_relax_factor",  1e-08); //Factor for initial relaxation of the bounds.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("check_derivatives_for_naninf",  "no"); //Indicates //whether it is desired to check for Nan / Inf in derivative matrices(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("chi_cup",  1.5); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("chi_hat",  2.0); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("chi_tilde",  5.0); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("compl_inf_tol",  0.0001); //Desired threshold for the complementarity conditions.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("constr_mult_init_max",  1000.0); //Maximum allowed least - square guess of constraint multipliers.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("constr_mult_reset_threshold",  0.0); //Threshold for resetting equality and inequality multipliers after restoration phase.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("constr_viol_tol",  0.0001); //Desired threshold for the constraint violation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("constraint_violation_norm_type",  "1-norm"); //- norm Norm to be used for the constraint violation in the line search.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("corrector_compl_avrg_red_fact",  1.0); //Complementarity tolerance factor for accepting corrector step(unsupported!).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("corrector_type",  "none"); //The //type of corrector steps that should be taken(unsupported!).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("delta",  1.0); //Multiplier for constraint violation in the switching rule.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("delta_y_max",  1e+12); //a parameter used to check if the fast direction can be used asthe line search direction(for Chen - Goldfarb line search).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("dependency_detection_with_rhs",  "no"); //Indicates if the right hand sides of the constraints should be considered during dependency detection(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("dependency_detector",  "none"); //Indicates //which linear solver should be used to detect linearly dependent equality constraints.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("derivative_test",  "none"); //Enable //derivative checker(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("derivative_test_first_index",  -2); //Index of first quantity to be checked by derivative checker(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("derivative_test_perturbation",  1e-08); //Size of the finite difference perturbation in derivative test.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("derivative_test_print_all",  "no"); //Indicates whether information for all estimated derivatives should be printed.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("derivative_test_tol",  0.0001); //Threshold for indicating wrong derivative.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("diverging_iterates_tol",  1e+20); //Threshold for maximal value of primal iterates.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("dual_inf_tol",  1.0); //Desired threshold for the dual infeasibility.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("epsilon_c",  0.01); //LIFENG //WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("eta_min",  10.0); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("eta_penalty",  1e-08); //Relaxation factor in the Armijo condition for the penalty function.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("eta_phi",  1e-08); //Relaxation factor in the Armijo condition.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("evaluate_orig_obj_at_resto_trial",  "yes"); //Determines //if the original objective function should be evaluated at restoration phase trial points.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("expect_infeasible_problem",  "no"); //Enable heuristics to quickly detect an infeasible problem.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("expect_infeasible_problem_ctol",  0.001); //Threshold for disabling "expect_infeasible_problem" option.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("expect_infeasible_problem_ytol",  100000000.0); //Multiplier threshold for activating "expect_infeasible_problem" option.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("fast_des_fact",  0.1); //a parameter used to check if the fast direction can be used asthe line search direction(for Chen - Goldfarb line search).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("fast_step_computation",  "no"); //Indicates if the linear system should be solved quickly.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("file_print_level",  5); //Verbosity //level for output file.(see IPOPT documentation CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("filter_margin_fact",  1e-05); //Factor determining width of margin for obj - constr - filter adaptive globalization strategy.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("filter_max_margin",  1.0); //Maximum width of margin in obj - constr - filter adaptive globalization strategy.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("filter_reset_trigger",  5); //Number //of iterations that trigger the filter reset.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("findiff_perturbation",  1e-07); //Size //of the finite difference perturbation for derivative approximation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("first_hessian_perturbation",  0.0001); //Size of first x - s perturbation tried.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("fixed_mu_oracle",  "average_compl"); //Oracle for the barrier parameter when switching to fixed mode.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("fixed_variable_treatment",  "make_parameter"); //Determines //how fixed variables should be handled.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("gamma_hat",  0.04); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("gamma_phi",  1e-08); //Relaxation factor in the filter margin for the barrier function.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("gamma_theta",  1e-05); //Relaxation factor in the filter margin for the constraint violation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("gamma_tilde",  4.0); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("hessian_approximation",  "exact"); //Indicates what Hessian information is to be used.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("hessian_constant",  "no"); //Indicates //whether the problem is a quadratic problem(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("honor_original_bounds",  "yes"); //Indicates whether final points should be projected into original bounds.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("inf_pr_output",  "original"); //Determines what value is printed in the "inf_pr" output column.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("jac_c_constant",  "no"); //Indicates whether all equality constraints are linear(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("jac_d_constant",  "no"); //Indicates whether all inequality constraints are linear(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("jacobian_approximation",  "exact"); //Specifies technique to compute constraint Jacobian(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("jacobian_regularization_exponent",  0.25); //Exponent for //mu in the regularization for rank - deficient constraint Jacobians.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("jacobian_regularization_value",  1e-08); //Size of the regularization for rank - deficient constraint Jacobians.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("kappa_d",  1e-05); //Weight for linear damping term(to handle one - sided bounds).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("kappa_sigma",  10000000000.0); //Factor limiting the deviation of dual variables from primal estimates.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("kappa_soc",  0.99); //Factor in the sufficient reduction rule for second order correction.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("kappa_x_dis",  100.0); //a parameter used to check if the fast direction can be used asthe line search direction(for Chen - Goldfarb line search).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("kappa_y_dis",  10000.0); //a parameter used to check if the fast direction can be used asthe line search direction(for Chen - Goldfarb line search).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("least_square_init_duals",  "no"); //Least square initialization of all dual variables(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("least_square_init_primal",  "no"); //Least square initialization of the primal variables(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("limited_memory_init_val",  1.0); //Value for B0 in low - rank update.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("limited_memory_init_val_max",  100000000.0); //Upper bound on value for B0 in low - rank update.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("limited_memory_init_val_min",  1e-08); //Lower bound on value for B0 in low - rank update.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("limited_memory_initialization",  "scalar1"); //Initialization strategy for the limited memory quasi - Newton approximation.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("limited_memory_max_history",  6); //Maximum size of the history for the limited quasi - Newton Hessian approximation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("limited_memory_max_skipping",  2); //Threshold for successive iterations where update is skipped.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("limited_memory_special_for_resto",  "no"); //Determines if the quasi - Newton updates should be special during the restoration phase.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("line_search_method",  "filter"); //Globalization method used in backtracking line search(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("linear_scaling_on_demand",  "yes"); //Flag indicating that linear scaling is only done if it seems required.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("ma27_ignore_singularity",  "no"); //Enables MA27's ability to solve a linear system even if the matrix is singular. (see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma27_la_init_factor",  5.0); //Real workspace memory for MA27.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma27_liw_init_factor",  5.0); //Integer workspace memory for MA27.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma27_meminc_factor",  10.0); //Increment factor for workspace size for MA27.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma27_pivtol",  1e-08); //Pivot tolerance for the linear solver MA27.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma27_pivtolmax",  0.0001); //Maximum pivot tolerance for the linear solver MA27.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("ma27_skip_inertia_check",  "no"); //Always pretend inertia is correct.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma28_pivtol",  0.01); //Pivot tolerance for linear solver MA28.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("ma57_automatic_scaling",  "yes"); //Controls MA57 automatic scaling(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("ma57_block_size",  16); //Controls block size used by Level 3 BLAS in MA57BD(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("ma57_node_amalgamation",  16); //Node amalgamation parameter(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("ma57_pivot_order",  5); //Controls //pivot order in MA57(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma57_pivtol",  1e-08); //Pivot tolerance for the linear solver MA57.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma57_pivtolmax",  0.0001); //Maximum pivot tolerance for the linear solver MA57.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma57_pre_alloc",  1.05); //Safety factor for work space memory allocation for the linear solver MA57.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("ma57_small_pivot_flag",  0); //If set to 1, then when small entries defined by CNTL(2) are detected they are removed and the corresponding pivots placed at the end of the factorization. This can be particularly efficient if the matrix is highly rank deficient.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("ma86_nemin",  32); //Node Amalgamation parameter(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("ma86_print_level",  0); //Debug printing level for the linear solver MA86(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma86_small",  1e-20); //Zero Pivot Threshold(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma86_static",  0.0); //Static Pivoting Threshold(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma86_u",  1e-08); //Pivoting Threshold(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("ma86_umax",  0.0001); //Maximum Pivoting Threshold(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("magic_steps",  "no"); //Enables magic steps.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("max_cpu_time",  1000000.0); //Maximum number of CPU seconds.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("max_filter_resets",  5); //Maximal allowed number of filter resets(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("max_hessian_perturbation",  1e+20); //Maximum //value of regularization parameter for handling negative curvature.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("max_iter",  3000); //Maximum number //of iterations.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("max_refinement_steps",  10); //Maximum //number of iterative refinement steps per linear system solve.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("max_resto_iter",  3000000); //Maximum number of successive iterations in restoration phase.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("max_soc",  4); //Maximum number of second order correction trial steps at each iteration.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("max_soft_resto_iters",  10); //Maximum //number of iterations performed successively in soft restoration phase.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("mehrotra_algorithm",  "no"); //Indicates if we want to do Mehrotra's algorithm. (see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("min_alpha_primal",  1e-13); //LIFENG //WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("min_hessian_perturbation",  1e-20); //Smallest //perturbation of the Hessian block.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("min_refinement_steps",  1); //Minimum //number of iterative refinement steps per linear system solve.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mu_init",  0.1); //Initial value for the barrier parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mu_linear_decrease_factor",  0.2); //Determines linear decrease rate of barrier parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mu_max",  100000.0); //Maximum value for barrier parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mu_max_fact",  1000.0); //Factor for initialization of maximum value for barrier parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mu_min",  1e-11); //Minimum value for barrier parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mu_superlinear_decrease_power",  1.5); //Determines superlinear decrease rate of barrier parameter.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mu_target",  0.0); //Desired value of complementarity.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mult_diverg_feasibility_tol",  1e-07); //tolerance for deciding if the multipliers are diverging(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mult_diverg_y_tol",  100000000.0); //tolerance for deciding if the multipliers are diverging(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mumps_dep_tol",  -1.0); //Pivot threshold for detection of linearly dependent constraints in MUMPS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("mumps_mem_percent",  1000); //Percentage //increase in the estimated working space for MUMPS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("mumps_permuting_scaling",  7); //Controls permuting and scaling in MUMPS(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("mumps_pivot_order",  7); //Controls pivot order in MUMPS(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mumps_pivtol",  1e-06); //Pivot tolerance for the linear solver MUMPS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("mumps_pivtolmax",  0.1); //Maximum pivot tolerance for the linear solver MUMPS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("mumps_scaling",  77); //Controls scaling in MUMPS(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("never_use_fact_cgpen_direction",  "no"); //Toggle to switch off the fast Chen - Goldfarb direction(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("never_use_piecewise_penalty_ls",  "no"); //Toggle to switch off the piecewise penalty method(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nlp_lower_bound_inf",  -1e+19); //any bound less or equal this value will be considered - inf(i.e. not lower bounded).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nlp_scaling_constr_target_gradient",  0.0); //Target value for constraint function gradient size.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nlp_scaling_max_gradient",  100.0); //Maximum //gradient after NLP scaling.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nlp_scaling_min_value",  1e-08); //Minimum value of gradient - based scaling values.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nlp_scaling_obj_target_gradient",  0.0); //Target value for objective function gradient size.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nlp_upper_bound_inf",  1e+19); //any bound greater or this value will be considered + inf(i.e. not upper bounded).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nu_inc",  0.0001); //Increment of the penalty parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("nu_init",  1e-06); //Initial value of the penalty parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("num_linear_variables",  0); // Number //of linear variables(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("obj_max_inc",  5.0); //Determines the upper bound on the acceptable increase of barrier objective function.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("obj_scaling_factor",  1.0); //Scaling factor for the objective function.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("pardiso_iter_coarse_size",  5000); //Maximum //Size of Coarse Grid Matrix(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("pardiso_iter_dropping_factor",  0.5); //dropping //value for incomplete factor(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("pardiso_iter_dropping_schur",  0.1); //dropping value for sparsify schur complement factor(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("pardiso_iter_inverse_norm_factor",  5000000.0); //(see //IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("pardiso_iter_max_levels",  10); //Maximum Size of Grid Levels(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("pardiso_iter_max_row_fill",  10000000); //max fill for each row(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("pardiso_iter_relative_tol",  1e-06); //Relative Residual Convergence(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("pardiso_iterative",  "no"); //Switch on iterative solver in Pardiso library(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("pardiso_matching_strategy",  "complete"); //+ 2x2Matching strategy to be used by Pardiso(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("pardiso_max_droptol_corrections",  4); //Maximal number of decreases of drop tolerance during one solve.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("pardiso_msglvl",  0); //Pardiso message level(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("pardiso_redo_symbolic_fact_only_if_inertia_wrong",  "no"); //Toggle //for handling case when elements were perturbed by Pardiso.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("pardiso_repeated_perturbation_means_singular",  "no"); //Interpretation //of perturbed elements.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("pardiso_skip_inertia_check",  "no"); //Always pretend inertia is correct.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("pen_des_fact",  0.2); //a parameter used in penalty parameter computation(for Chen - Goldfarb line search).(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("pen_init_fac",  50.0); //a parameter used to choose initial penalty parameterswhen the regularized Newton method is used.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("pen_theta_max_fact",  10000.0); //Determines upper bound for constraint violation in the filter.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("penalty_init_max",  100000.0); //Maximal value for the intial penalty parameter(for Chen - Goldfarb line search).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("penalty_init_min",  1.0); //Minimal value for the intial penalty parameter for line search(for Chen - Goldfarb line search).(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("penalty_max",  1e+30); //Maximal value for the penalty parameter(for Chen - Goldfarb line search).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("penalty_update_compl_tol",  10.0); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("penalty_update_infeasibility_tol",  1e-09); // Threshold for infeasibility in penalty parameter update test.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("perturb_always_cd",  "no"); //Active permanent perturbation of constraint linearization.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("perturb_dec_fact",  0.333333333333); //Decrease //factor for x - s perturbation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("perturb_inc_fact",  8.0); //Increase factor for x - s perturbation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("perturb_inc_fact_first",  100.0); //Increase factor for x - s perturbation for very first perturbation.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("piecewisepenalty_gamma_infeasi",  1e-13); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("piecewisepenalty_gamma_obj",  1e-13); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("point_perturbation_radius",  10.0); //Maximal perturbation of an evaluation point.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("print_info_string",  "no"); //Enables printing of additional info string at end of iteration output.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("print_level",  0); //Output verbosity level.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("print_options_documentation",  "no"); //Switch to print all algorithmic options.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("print_options_latex_mode",  "no"); //Undocumented(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("print_timing_statistics",  "no"); //Switch to print timing statistics.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("print_user_options",  "no"); //Print all options set by the user.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("quality_function_balancing_term",  "none"); //The balancing term included in the quality function for centrality.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("quality_function_centrality",  "none"); //The penalty term for centrality that is included in quality function.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("quality_function_max_section_steps",  8); //Maximum number of search steps during direct search procedure determining the optimal centering parameter.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("quality_function_section_qf_tol",  0.0); //Tolerance for the golden section search procedure determining the optimal centering parameter(in the function value space).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("quality_function_section_sigma_tol",  0.01); //Tolerance for the section search procedure determining the optimal centering parameter(in sigma space).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("recalc_y",  "no"); //Tells the algorithm to recalculate the equality and inequality multipliers as least square estimates.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("recalc_y_feas_tol",  1e-06); //Feasibility threshold for recomputation of multipliers.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("replace_bounds",  "no"); //Indicates if all variable bounds should be replaced by inequality constraints(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("required_infeasibility_reduction",  0.9); //Required reduction of infeasibility before leaving restoration phase.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("residual_improvement_factor",  0.999999999); //Minimal required reduction of residual test ratio in iterative refinement.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("residual_ratio_max",  1e-10); //Iterative refinement tolerance(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("residual_ratio_singular",  1e-05); //Threshold for declaring linear system singular after failed iterative refinement.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("resto_failure_feasibility_threshold",  0.0); //Threshold for primal infeasibility to declare failure of restoration phase.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("resto_penalty_parameter",  1000.0); //Penalty parameter in the restoration phase objective function.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("resto_proximity_weight",  1.0); //Weighting factor for the proximity term in restoration phase objective.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("rho",  0.1); //Value in penalty parameter update formula.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("s_max",  100.0); //Scaling threshold for the NLP error.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("s_phi",  2.3); //Exponent for linear barrier function model in the switching rule.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("s_theta",  1.1); //Exponent for current constraint violation in the switching rule.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("sb",  "yes"); //(see IPOPT documentation CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("sigma_max",  100.0); //Maximum value of the centering parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("sigma_min",  1e-06); //Minimum value of the centering parameter.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("skip_corr_if_neg_curv",  "yes"); //Skip the corrector step in negative curvature iteration(unsupported!).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("skip_corr_in_monotone_mode",  "yes"); //Skip the corrector step during monotone barrier parameter mode(unsupported!).(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("skip_finalize_solution_call",  "no"); //Indicates if call to NLP::FinalizeSolution after optimization should be suppressed(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("slack_bound_frac",  0.01); //Desired minimum relative distance from the initial slack to bound.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("slack_bound_push",  0.01); //Desired minimum absolute distance from the initial slack to bound.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("slack_move",  1.81898940355e-12); //Correction size for very small slacks.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("soft_resto_pderror_reduction_factor",  0.9999); //Required reduction in primal - dual error in the soft restoration phase.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("start_with_resto",  "no"); //Tells algorithm to switch to restoration phase in first iteration.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("suppress_all_output",  "no"); //Undocumented(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("tau_min",  0.99); //Lower bound on fraction - to - the - boundary parameter tau.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("theta_max_fact",  10000.0); //Determines upper bound for constraint violation in the filter.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("theta_min",  1e-06); //LIFENG WRITES THIS.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("theta_min_fact",  0.0001); //Determines constraint violation threshold in the switching rule.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("tiny_step_tol",  2.22044604925e-15); //Tolerance for detecting numerically insignificant steps.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("tiny_step_y_tol",  0.01); //Tolerance for quitting because of numerically insignificant steps.(see IPOPT documentation)CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("tol",  1e-08); //Desired convergence tolerance(relative).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("vartheta",  0.5); //a parameter used to check if the fast direction can be used asthe line search direction(for Chen - Goldfarb line search).(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("warm_start_bound_frac",  0.001); //same as bound_frac for the regular initializer.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("warm_start_bound_push",  0.001); //same as bound_push for the regular initializer.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("warm_start_entire_iterate",  "no"); //Tells algorithm whether to use the GetWarmStartIterate method in the NLP.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("warm_start_init_point",  "no"); //Warm - start for initial point(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("warm_start_mult_bound_push",  0.001); //same as mult_bound_push for the regular initializer.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("warm_start_mult_init_max",  1000000.0); //Maximum initial value for the equality multipliers.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetStringValue("warm_start_same_structure",  "no"); //Indicates whether a problem with a structure identical to the previous one is to be solved.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("warm_start_slack_bound_frac",  0.001); //same as slack_bound_frac for the regular initializer.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("warm_start_slack_bound_push",  0.001); //same as slack_bound_push for the regular initializer.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetNumericValue("warm_start_target_mu",  0.0); //Unsupported!(see //IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("watchdog_shortened_iter_trigger",  10); //Number of shortened iterations that trigger the watchdog.(see IPOPT documentation) CasADi::IpoptInternal
    (*app)->Options()->SetIntegerValue("watchdog_trial_iter_max",  3); //Maximum number of watchdog iterations.(see IPOPT documentation)CasADi::IpoptInternal
    //app->Options()->SetNumericValue("wsmp_inexact_droptol",  0.0); //Drop //tolerance for inexact factorization preconditioner in WISMP.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetNumericValue("wsmp_inexact_fillin_limit",  0.0); //Fill - in limit for inexact factorization preconditioner in WISMP.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("wsmp_iterative",  "no"); //Switches to iterative solver in WSMP.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetIntegerValue("wsmp_max_iter",  1000); //Maximal //number of iterations in iterative WISMP(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("wsmp_no_pivoting",  "no"); //Use //the static pivoting option of WSMP.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetIntegerValue("wsmp_num_threads",  1); //Number //of threads to be used in WSMP(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetIntegerValue("wsmp_ordering_option",  1); //Determines how ordering is done in WSMP(IPARM(16)(see IPOPT documentation)CasADi::IpoptInternal
    // app->Options()->SetIntegerValue("wsmp_ordering_option2",  1); //Determines how ordering is done in WSMP(IPARM(20)(see IPOPT documentation)CasADi::IpoptInternal
    // app->Options()->SetNumericValue("wsmp_pivtol",  0.0001); //Pivot tolerance for the linear solver WSMP.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetNumericValue("wsmp_pivtolmax",  0.1); //Maximum pivot tolerance for the linear solver WSMP.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetIntegerValue("wsmp_scalingInteger",  0); //Determines how the matrix is scaled by WSMP.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetNumericValue("wsmp_singularity_threshold",  1e-18); //WSMP's singularity threshold. (see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("wsmp_skip_inertia_check",  "no"); //Always pretent inertia is correct.(see IPOPT documentation/CasADi::IpoptInternal
    // app->Options()->SetIntegerValue("wsmp_write_matrix_iteration",  -1); //Iteration in which the matrices are written to files.(see IPOPT documentation) CasADi::IpoptInternal}kj   app->Options()->SetIntegerValue("print_level", 0);
    // app->Options()->SetOT_BOOLEANValue("print_time",  true); //The information about execution time CasADi::IpoptInternal
    // app->Options()->SetStringValue("quality_function_norm_type",  "2"); //- norm - squared Norm used for components of the quality function.(see IPOPT documentation) CasADi::IpoptInternal
    /* app->Options()->SetOT_BOOLEANValue("regularity_check",  trueThrow); //exceptions when NaN or Inf appears during evaluation CasADi::FunctionInternal */
    // app->Options()->SetIntegerValue("pardiso_out_of_core_power",  0); //Enables out - of - core variant of Pardiso(see IPOPT documentation)CasADi::IpoptInternal
    /* app->Options()->Set500Value("pardiso_max_iterInteger",  Maximum); //number of Krylov - Subspace Iteration(see IPOPT documentation) CasADi::IpoptInternal */
    // app->Options()->SetOT_BOOLEANValue("pass_nonlinear_variables",  false); //n a CasADi::IpoptInternal
    // app->Options()->SetStringValue("fixed_variable_treatment", "fixed_variable_treatment");
    // app->Options()->SetStringValue("ad_mode",  "automatic"); //How to calculate the Jacobians.(forward : only forward mode | reverse : only adjoint mode | automatic : a heuristic decides which is more appropriate)CasADi::FunctionInternal
    // app->Options()->SetStringValue("adaptive_mu_globalization",  "obj"); //- constr - filter Globalization strategy for the adaptive mu selection mode.(see IPOPT documentation)CasADi::IpoptInternal
    // app->Options()->SetStringValue("adaptive_mu_kkt_norm_type",  "2"); //- norm - squared Norm used for the KKT error in the adaptive mu globalization strategies.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("bound_mult_init_method",  "constantInitialization"); //method for bound multipliers(see IPOPT documentation) CasADi::IpoptInternal
    /* app->Options()->SetOT_DICTIONARYValue("con_integer_md",  None); //Integer metadata(a dictionary with lists of integers) about constraints to be passed to IPOPT CasADi::IpoptInternal */
    /* app->Options()->SetOT_DICTIONARYValue("con_numeric_md",  None); //Numeric metadata(a dictionary with lists of reals) about constraints to be passed to IPOPT CasADi::IpoptInternal */
    /* app->Options()->SetOT_DICTIONARYValue("con_string_md",  None); //String metadata(a dictionary with lists of strings) about constraints to be passed to IPOPTCasADi::IpoptInternal */
    /* app->Options()->SetOT_DERIVATIVEGENERATORValue("derivative_generator",  GenericType()); //Function that returns a derivative function given a number of forward and reverse directional derivative, overrides internal routines. Check documentation of DerivativeGenerator. CasADi::FunctionInternal */
    // app->Options()->SetOT_BOOLEANValue("expand",  false); //Expand the NLP function in terms of scalar operations, i.e. MX->SX CasADi::NLPSolverInternal
    /* app->Options()->SetOT_BOOLEANValue("expand_f",  GenericType()); //Expand //the objective function in terms of scalar operations, i.e. MX->SX. Deprecated, use "expand" instead. CasADi::NLPSolverInternal */
    /* app->Options()->SetOT_BOOLEANValue("expand_g",  GenericType()); //Expand //the constraint function in terms of scalar operations, i.e. MX->SX. Deprecated, use "expand" instead.CasADi::NLPSolverInternal */
    // app->Options()->SetOT_BOOLEANValue("gather_stats",  false); //Flag //to indicate wether statistics must be gathered CasADi::FunctionInternal
    /* app->Options()->SetOT_BOOLEANValue("gauss_newton",  GenericType()); //Deprecated //option. Use Gauss Newton Hessian approximation CasADi::NLPSolverInternal */
    /* app->Options()->SetOT_BOOLEANValue("generate_gradient",  GenericType()); //Deprecated option. Generate a function for calculating the gradient of the objective. CasADi::NLPSolverInternal */
    /* app->Options()->SetOT_BOOLEANValue("generate_hessian",  GenericType()); // Deprecated //option. Generate an exact Hessian of the Lagrangian if not supplied. CasADi::NLPSolverInternal */
    /* app->Options()->SetOT_BOOLEANValue("generate_jacobian",  GenericType()); //Deprecated option. Generate an exact Jacobian of the constraints if not supplied. CasADi::NLPSolverInternal */
    /* app->Options()->SetOT_FunctionValue("grad_f",  NoneFunction); //for calculating the gradient of the objective(column, autogenerated by default) CasADi::IpoptInternal */
    /* app->Options()->SetOT_FunctionValue("grad_lag",  NoneFunction); //for //calculating the gradient of the Lagrangian(autogenerated by default) CasADi::IpoptInternal */
    /* app->Options()->SetOT_FunctionValue("hess_lag",  NoneFunction); //for //calculating the Hessian of the Lagrangian(autogenerated by default) CasADi::IpoptInternal */
    // app->Options()->SetStringValue("hessian_approximation_space",  "nonlinear"); //- variables Indicates in which subspace the Hessian information is to be approximated.(see IPOPT documentation)CasADi::IpoptInternal
    // app->Options()->SetOT_BOOLEANValue("ignore_check_vec",  false); //If set to true, the input shape of F will not be checked. CasADi::NLPSolverInternal
    /* app->Options()->SettrueThrowValue("inputs_checkOT_BOOLEAN",  exceptions); //when the numerical values of the inputs don't make sense    CasADi::FunctionInternal */
    /* app->Options()->SetOT_CALLBACKValue("iteration_callback",  GenericType()); //A function that will be called at each iteration with the solver as input. Check documentation of Callback. CasADi::NLPSolverInternal */
    // app->Options()->SetOT_BOOLEANValue("iteration_callback_ignore_errors",  false); //If set to true, errors thrown by iteration_callback will be ignored.CasADi::NLPSolverInternal
    // app->Options()->SetIntegerValue("iteration_callback_step",  1); //Only call the callback function every few iterations. CasADi::NLPSolverInternal
    /* app->Options()->SetOT_FunctionValue("jac_f",  None); //Function //for calculating the jacobian of the objective(sparse row, autogenerated by default) CasADi::IpoptInternal */
    /* app->Options()->SetOT_FunctionValue("jac_g",  None); //Function //for calculating the Jacobian of the constraints(autogenerated by default) CasADi::IpoptInternal */
    // app->Options()->SetStringValue("limited_memory_aug_solver",  "sherman"); //- morrisonStrategy for solving the augmented system for low - rank Hessian.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("limited_memory_update_type",  "bfgsQuasi"); //- Newton update formula for the limited memory approximation.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("linear_solver",  "ma27Linear"); //solver used for step computations.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("linear_system_scaling",  "mc19"); //Method for scaling the linear system.(see IPOPT documentation) CasADi::IpoptInternal
    /* app->Options()->SetStringVECTORValue("monitor",  GenericType()); //Monitors to be activated(inputs | outputs) */
//app->Options()->Set| eval_gValue("(eval_f",  //|); eval_jac_g | eval_grad_f | eval_h) CasADi::FunctionInternal
    // app->Options()->Setmu_allow_fast_monotone_decreaseValue("CasADi::IpoptInternal",
    //         String); //yes Allow skipping of barrier problem if barrier test is already met.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("mu_oracle",  "quality"); //- functionOracle for a new barrier parameter in the adaptive strategy.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("mu_strategy",  "monotoneUpdate"); //strategy for barrier parameter.(see IPOPT documentation)CasADi::IpoptInternal
    // app->Options()->SetStringValue("name",  "unnamed_shared_object"); //name //of the object CasADi::OptionsFunctionalityNode
    // app->Options()->SetNumericValue("neg_curv_test_tol",  0.0); //Tolerance for heuristic to ignore wrong inertia.(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("nlp_scaling_method",  "gradient"); //- based Select the technique used for scaling the NLP.(see IPOPT documentation)CasADi::IpoptInternal
    // app->Options()->SetStringValue("option_file_name",  "File"); //name of options file(to overwrite default).(see IPOPT documentation) CasADi::IpoptInternal
    // app->Options()->SetStringValue("output_file",  "File"); //name of desired output file(leave unset for no file output).(see IPOPT documentation)CasADi::IpoptInternal
    /* app->Options()->SetOT_BOOLEANValue("parametric",  GenericType()); //Deprecated option. Expect F, G, H, J to have an additional input argument appended at the end, denoting fixed parameters. CasADi::NLPSolverInternal */
    /* app->Options()->SetOT_VOIDPTRValue("user_data",  GenericType()); //A user - defined field that can be used to identify the function or pass additional information CasADi::FunctionInternal */
    /* app->Options()->SetOT_DICTIONARYValue("var_integer_md",  None); //Integer metadata(a dictionary with lists of integers) about variables to be passed to IPOPTCasADi::IpoptInternal */
    /* app->Options()->SetOT_DICTIONARYValue("var_numeric_md",  None); //Numeric metadata(a dictionary with lists of reals) about variables to be passed to IPOPT CasADi::IpoptInternal */
    /* app->Options()->SetOT_DICTIONARYValue("var_string_md",  None); //String metadata(a dictionary with lists of strings) about variables to be passed to IPOPT CasADi::IpoptInternal */
    // app->Options()->SetOT_BOOLEANValue("warn_initial_bounds",  false); //Warn iVf the initial guess does not satisfy LBX and UBX CasADi::NLPSolverInternal
    // app->Options()->SetOT_BOOLEANValue("verbose",  false); //Verbose evaluation – for debuggingCasADi::FunctionInternal
}
