__author__ = 'sibirrer'

#this file contains a class to compute the Navaro-Frank-White function in mass/kappa space
#the potential therefore is its integral

import numpy as np

class NFW(object):
    """
    this class contains functions concerning the NFW profile

    relation are: R_200 = c * Rs
    """

    def function(self, x, y, Rs, theta_Rs, center_x=0, center_y=0):
        """
        
        :param x: angular position
        :param y: angular position
        :param Rs: angular turn over point 
        :param theta_Rs: deflection at Rs
        :param center_x: center of halo
        :param center_y: center of halo
        :return: 
        """
        rho0_input = self._alpha2rho0(theta_Rs=theta_Rs, Rs=Rs)
        if Rs < 0.0001:
            Rs = 0.0001
        x_ = x - center_x
        y_ = y - center_y
        R = np.sqrt(x_**2 + y_**2)
        f_ = self.nfwPot(R, Rs, rho0_input)
        return f_

    def derivatives(self, x, y, Rs, theta_Rs, center_x=0, center_y=0):
        """
        returns df/dx and df/dy of the function (integral of NFW)
        """
        rho0_input = self._alpha2rho0(theta_Rs=theta_Rs, Rs=Rs)
        if Rs < 0.0001:
            Rs = 0.0001
        x_ = x - center_x
        y_ = y - center_y
        R = np.sqrt(x_**2 + y_**2)
        f_x, f_y = self.nfwAlpha(R, Rs, rho0_input, x_, y_)
        return f_x, f_y

    def hessian(self, x, y, Rs, theta_Rs, center_x=0, center_y=0):
        """
        returns Hessian matrix of function d^2f/dx^2, d^f/dy^2, d^2/dxdy
        """
        rho0_input = self._alpha2rho0(theta_Rs=theta_Rs, Rs=Rs)
        if Rs < 0.0001:
            Rs = 0.0001
        x_ = x - center_x
        y_ = y - center_y
        R = np.sqrt(x_**2 + y_**2)
        kappa = self.density_2d(R, 0, Rs, rho0_input)
        gamma1, gamma2 = self.nfwGamma(R, Rs, rho0_input, x_, y_)
        f_xx = kappa + gamma1
        f_yy = kappa - gamma1
        f_xy = gamma2
        return f_xx, f_yy, f_xy

    def density(self, R, Rs, rho0):
        """
        three dimenstional NFW profile

        :param R: radius of interest
        :type R: float/numpy array
        :param Rs: scale radius
        :type Rs: float
        :param rho0: density normalization (characteristic density)
        :type rho0: float
        :return: rho(R) density
        """
        return rho0/(R/Rs*(1+R/Rs)**2)

    def density_2d(self, x, y, Rs, rho0, center_x=0, center_y=0):
        """
        projected two dimenstional NFW profile (kappa*Sigma_crit)

        :param R: radius of interest
        :type R: float/numpy array
        :param Rs: scale radius
        :type Rs: float
        :param rho0: density normalization (characteristic density)
        :type rho0: float
        :param r200: radius of (sub)halo
        :type r200: float>0
        :return: Epsilon(R) projected density at radius R
        """
        x_ = x - center_x
        y_ = y - center_y
        R = np.sqrt(x_**2 + y_**2)
        x = R/Rs
        Fx = self._F(x)
        return 2*rho0*Rs*Fx

    def mass_3d(self, R, Rs, rho0):
        """
        mass enclosed a 3d sphere or radius r
        :param r:
        :param Ra:
        :param Rs:
        :return:
        """
        Rs = float(Rs)
        m_3d = 4. * np.pi * rho0 * Rs**3 *(np.log((Rs + R)/Rs) - R/(Rs + R))
        return m_3d

    def mass_3d_lens(self, R, Rs, theta_Rs):
        """
        mass enclosed a 3d sphere or radius r
        :param r:
        :param Ra:
        :param Rs:
        :return:
        """
        rho0 = self._alpha2rho0(theta_Rs, Rs)
        m_3d = self.mass_3d(R, Rs, rho0)
        return m_3d

    def mass_2d(self, R, Rs, rho0):
        """
        mass enclosed a 3d sphere or radius r
        :param r:
        :param Ra:
        :param Rs:
        :return:
        """
        x = R/Rs
        gx = self._g(x)
        m_2d = 4*rho0*Rs*R**2*gx/x**2 * np.pi
        return m_2d

    def nfwPot(self, R, Rs, rho0):
        """
        lensing potential of NFW profile (*Sigma_crit*D_OL**2)

        :param R: radius of interest
        :type R: float/numpy array
        :param Rs: scale radius
        :type Rs: float
        :param rho0: density normalization (characteristic density)
        :type rho0: float
        :param r200: radius of (sub)halo
        :type r200: float>0
        :return: Epsilon(R) projected density at radius R
        """
        x=R/Rs
        hx=self._h(x)
        return 2*rho0*Rs**3*hx

    def nfwAlpha(self, R, Rs, rho0, ax_x, ax_y):
        """
        deflection angel of NFW profile (*Sigma_crit*D_OL) along the projection to coordinate "axis"

        :param R: radius of interest
        :type R: float/numpy array
        :param Rs: scale radius
        :type Rs: float
        :param rho0: density normalization (characteristic density)
        :type rho0: float
        :param r200: radius of (sub)halo
        :type r200: float>0
        :param axis: projection to either x- or y-axis
        :type axis: same as R
        :return: Epsilon(R) projected density at radius R
        """
        if isinstance(R, int) or isinstance(R, float):
            R = max(R, 0.00001)
        else:
            R[R <= 0.00001] = 0.00001
        x = R/Rs
        gx = self._g(x)
        a = 4*rho0*Rs*R*gx/x**2/R
        return a*ax_x, a*ax_y

    def nfwGamma(self, R, Rs, rho0, ax_x, ax_y):
        """
        shear gamma of NFW profile (*Sigma_crit) along the projection to coordinate "axis"

        :param R: radius of interest
        :type R: float/numpy array
        :param Rs: scale radius
        :type Rs: float
        :param rho0: density normalization (characteristic density)
        :type rho0: float
        :param r200: radius of (sub)halo
        :type r200: float>0
        :param axis: projection to either x- or y-axis
        :type axis: same as R
        :return: Epsilon(R) projected density at radius R
        """
        c = 0.001
        if isinstance(R, int) or isinstance(R, float):
            R = max(R, c)
        else:
            R[R <= c] = c
        x = R/Rs
        gx = self._g(x)
        Fx = self._F(x)
        a = 2*rho0*Rs*(2*gx/x**2 - Fx)#/x #2*rho0*Rs*(2*gx/x**2 - Fx)*axis/x
        return a*(ax_y**2-ax_x**2)/R**2, -a*2*(ax_x*ax_y)/R**2

    def _F(self, X):
        """
        analytic solution of the projection integral

        :param x: R/Rs
        :type x: float >0
        """
        if isinstance(X, int) or isinstance(X, float):
            if X < 1 and X > 0:
                a = 1/(X**2-1)*(1-2/np.sqrt(1-X**2)*np.arctanh(np.sqrt((1-X)/(1+X))))
            elif X == 1:
                a = 1./3
            elif X > 1:
                a = 1/(X**2-1)*(1-2/np.sqrt(X**2-1)*np.arctan(np.sqrt((X-1)/(1+X))))
            else:  # X == 0:
                c = 0.0001
                a = 1/(-1)*(1-2/np.sqrt(1)*np.arctanh(np.sqrt((1-c)/(1+c))))

        else:
            a = np.empty_like(X)
            x = X[X < 1]
            a[X<1] = 1/(x**2-1)*(1-2/np.sqrt(1-x**2)*np.arctanh(np.sqrt((1-x)/(1+x))))

            x = X[X == 1]
            a[X==1] = 1./3.

            x = X[X > 1]
            a[X>1] = 1/(x**2-1)*(1-2/np.sqrt(x**2-1)*np.arctan(np.sqrt((x-1)/(1+x))))
            # a[X>y] = 0

            c = 0.001
            x = X[X == 0]
            a[X==0] = 1/(-1)*(1-2/np.sqrt(1)*np.arctanh(np.sqrt((1-c)/(1+c))))
        return a

    def _g(self, X):
        """
        analytic solution of integral for NFW profile to compute deflection angel and gamma

        :param x: R/Rs
        :type x: float >0
        """
        c = 0.001
        if isinstance(X, int) or isinstance(X, float):
            if X < 1:
                x = max(c, X)
                a = np.log(x/2.) + 1/np.sqrt(1-x**2)*np.arccosh(1./x)
            elif X == 1:
                a = 1 + np.log(1./2.)
            else:  # X > 1:
                a = np.log(X/2) + 1/np.sqrt(X**2-1)*np.arccos(1./X)

        else:
            a = np.empty_like(X)
            X[X <= c] = c
            x = X[X < 1]

            a[X < 1] = np.log(x/2.) + 1/np.sqrt(1-x**2)*np.arccosh(1./x)

            a[X == 1] = 1 + np.log(1./2.)

            x = X[X > 1]
            a[X > 1] = np.log(x/2) + 1/np.sqrt(x**2-1)*np.arccos(1./x)

        return a

    def _h(self, X):
        """
        analytic solution of integral for NFW profile to compute the potential

        :param x: R/Rs
        :type x: float >0
        """
        c = 0.001
        if isinstance(X, int) or isinstance(X, float):
            if X < 1:
                x = max(0.001, X)
                a = np.log(x/2.)**2 - np.arccosh(1./x)**2
            else:  # X >= 1:
                a = np.log(X/2.)**2 + np.arccos(1./X)**2
        else:
            a = np.empty_like(X)
            X[X <= c] = 0.001
            x = X[X < 1]
            a[X < 1] = np.log(x/2.)**2 - np.arccosh(1./x)**2
            x = X[X >= 1]
            a[X >= 1] = np.log(x/2.)**2 + np.arccos(1./x)**2
        return a

    def _alpha2rho0(self, theta_Rs, Rs):
        """
        convert angle at Rs into rho0
        """
        rho0 = theta_Rs / (4. * Rs ** 2 * (1. + np.log(1. / 2.)))
        return rho0

    def _rho02alpha(self, rho0, Rs):
        """
        convert rho0 to angle at Rs
        :param rho0:
        :param Rs:
        :return:
        """
        theta_Rs = rho0 * (4 * Rs ** 2 * (1 + np.log(1. / 2.)))
        return theta_Rs


