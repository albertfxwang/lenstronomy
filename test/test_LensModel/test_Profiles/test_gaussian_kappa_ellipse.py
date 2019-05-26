__author__ = 'ajshajib'

from lenstronomy.LensModel.Profiles.gaussian_kappa_ellipse import GaussianKappaEllipse
from lenstronomy.LensModel.Profiles.gaussian_kappa import GaussianKappa

import numpy as np
import numpy.testing as npt
from scipy.special import expi
import pytest


class TestGaussianKappaEllipse(object):
    """
    test the Gaussian with Gaussian kappa
    """
    def setup(self):
        self.gaussian_kappa = GaussianKappa()
        self.ellipse = GaussianKappaEllipse()

    def test_function(self):
        x = 1
        y = 1
        e1, e2 = 5e-5, 0
        sigma = 1
        amp = 2

        f_ = self.ellipse.function(x, y, amp, sigma, e1, e2)

        r2 = x*x + y*y
        f_sphere = amp/(2*np.pi*sigma**2) * sigma**2 * (np.euler_gamma -
                        expi(-r2/2/sigma**2) + np.log(r2/2/sigma**2))
        npt.assert_almost_equal(f_, f_sphere, decimal=4)

    def test_derivatives(self):
        x = 1
        y = 1
        e1, e2 = 5e-5, 0
        sigma = 1
        amp = 2
        f_x, f_y = self.ellipse.derivatives(x, y, amp, sigma, e1, e2)
        f_x_sphere, f_y_sphere = self.gaussian_kappa.derivatives(x, y, amp=amp,
                                                                 sigma=sigma)
        npt.assert_almost_equal(f_x, f_x_sphere, decimal=4)
        npt.assert_almost_equal(f_y, f_y_sphere, decimal=4)

    def test_hessian(self):
        x = 1
        y = 1
        e1, e2 = 5e-5, 0
        sigma = 1
        amp = 2
        f_xx, f_yy, f_xy = self.ellipse.hessian(x, y, amp, sigma, e1, e2)
        f_xx_sphere, f_yy_sphere, f_xy_sphere = self.gaussian_kappa.hessian(x, y, amp=amp, sigma=sigma)
        npt.assert_almost_equal(f_xx, f_xx_sphere, decimal=4)
        npt.assert_almost_equal(f_yy, f_yy_sphere, decimal=4)
        npt.assert_almost_equal(f_xy, f_xy_sphere, decimal=4)

    def test_density_2d(self):
        x = 1
        y = 1
        e1, e2 = 5e-5, 0
        sigma = 1
        amp = 2
        f_ = self.ellipse.density_2d(x, y, amp, sigma, e1, e2)
        f_sphere = amp / (2*np.pi*sigma**2) * np.exp(-(x*x+y*y)/2/sigma**2)
        npt.assert_almost_equal(f_, f_sphere, decimal=4)


if __name__ == '__main__':
    pytest.main()