
import numpy as np
from EconModel import EconModelClass
from GEModelTools import GEModelClass

import household_problem
import steady_state
import blocks

class HANKModelClass(EconModelClass,GEModelClass):
    
    #########
    # setup #
    #########      

    def settings(self):
        """ fundamental settings """

        # a. namespaces
        self.namespaces = ['par','ss','ini','path','sim']
        
        # b. household
        self.grids_hh = ['a'] # grids
        self.pols_hh = ['a'] # policy functions
        self.inputs_hh = ['w','r','d','tau'] # direct inputs
        self.inputs_hh_z = [] # transition matrix inputs
        self.outputs_hh = ['a','c','ne'] # outputs
        self.intertemps_hh = ['vbeg_a'] # intertemporal variables

        # c. GE
        self.shocks = ['istar','Z'] # exogenous inputs
        self.unknowns = ['pi','w','Y'] # endogenous inputs
        self.targets = ['nkpc_res','clearing_A','clearing_NE'] # targets
        
        # d. all variables
        self.varlist = [ # all variables
            'A_hh',
            'A',
            'B',
            'C_hh',
            'C',
            'clearing_A',
            'clearing_C',
            'clearing_NE',
            'd',
            'G',
            'i',
            'NE_hh',
            'NE',
            'nkpc_res',
            'pi',
            'psi',
            'r',
            'istar',
            'tau',
            'w',
            'Y',
            'Z',
        ]

        # e. functions
        self.solve_hh_backwards = household_problem.solve_hh_backwards
        self.block_pre = blocks.block_pre
        self.block_post = blocks.block_post
        
    def setup(self):
        """ set baseline parameters """

        par = self.par

        par.Nfix = 1
        par.r_target_ss = 0.005

        # a. preferences
        par.beta = 0.98 # discount factor (guess, calibrated in ss)
        par.varphi = 0.80 # disutility of labor (guess, calibrated in ss)

        par.sigma = 2.0 # inverse of intertemporal elasticity of substitution
        par.nu = 2.0 # inverse Frisch elasticity
        
        # c. income parameters
        par.rho_e = 0.966 # AR(1) parameter
        par.sigma_e = 0.50 # std. of e
        par.Ne = 7 # number of productivity states

        # d. price setting
        par.mu = 1.2 # mark-up
        par.kappa = 0.1 # slope of Phillips curve

        # e. government
        par.phi = 1.5 # Taylor rule coefficient on inflation
        par.phi_y = 0.0 # Taylor rule coefficient on output
        
        par.G_target_ss = 0.0 # government spending
        par.B_target_ss = 5.6 # bond supply

        par.tau_r_fac = 1.0 # effect of r changes on taxes
        
        # f. grids         
        par.a_min = 0.0 # maximum point in grid for a
        par.a_max = 150.0 # maximum point in grid for a
        par.Na = 500 # number of grid points

        # g. shocks
        par.jump_Z = 0.0 # initial jump in %
        par.jump_istar = -0.0025
        par.rho_Z = 0.00 # AR(1) coefficeint
        par.rho_istar = 0.61

        # h. misc.
        par.T = 500 # length of path        
        
        par.max_iter_solve = 50_000 # maximum number of iterations when solving
        par.max_iter_simulate = 50_000 # maximum number of iterations when simulating
        par.max_iter_broyden = 100 # maximum number of iteration when solving eq. system
        
        par.tol_ss = 1e-11 # tolerance when finding steady state
        par.tol_solve = 1e-11 # tolerance when solving
        par.tol_simulate = 1e-11 # tolerance when simulating
        par.tol_broyden = 1e-10 # tolerance when solving eq. system
        
    def allocate(self):
        """ allocate model """

        par = self.par

        par.Nz = par.Ne

        # b. solution
        self.allocate_GE()

    prepare_hh_ss = steady_state.prepare_hh_ss
    find_ss = steady_state.find_ss        