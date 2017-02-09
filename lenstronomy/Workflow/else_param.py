import astrofunc.util as util
import numpy as np


class ElseParam(object):
    """

    """

    def __init__(self, kwargs_options, kwargs_fixed):
        self.kwargs_options = kwargs_options
        self.kwargs_fixed = kwargs_fixed
        self.num_images = kwargs_options.get('num_images', 4)
        self.external_shear = kwargs_options.get('external_shear', False)
        self.foreground_shear = kwargs_options.get('foreground_shear', False) \
                                and kwargs_options.get('external_shear', False)

    def getParams(self, args, i):
        """

        :param args:
        :param i:
        :return:
        """
        kwargs = {}
        if not 'ra_pos' in self.kwargs_fixed:
            kwargs['ra_pos'] = np.array(args[i:i+self.num_images])
            i += self.num_images
        if not 'dec_pos' in self.kwargs_fixed:
            kwargs['dec_pos'] = np.array(args[i:i+self.num_images])
            i += self.num_images
        if self.kwargs_options.get('image_plane_source', False):
            if not 'source_pos_image_ra' in self.kwargs_fixed:
                kwargs['source_pos_image_ra'] = args[i]
                i += 1
            if not 'source_pos_image_dec' in self.kwargs_fixed:
                kwargs['source_pos_image_dec'] = args[i]
                i += 1
        if self.external_shear:
            if not 'gamma1' in self.kwargs_fixed or not 'gamma2' in self.kwargs_fixed:
                kwargs['gamma1'] = args[i]
                kwargs['gamma2'] = args[i+1]
                i += 2
        if self.foreground_shear:
            if not 'gamma1_foreground' in self.kwargs_fixed or not 'gamma2_foreground' in self.kwargs_fixed:
                kwargs['gamma1_foreground'] = args[i]
                kwargs['gamma2_foreground'] = args[i+1]
                i += 2
        if self.kwargs_options.get('time_delay', False) is True:
            if not 'delay_dist' in self.kwargs_fixed:
                kwargs['delay_dist'] = args[i]
                i += 1
        if not 'shapelet_beta' in self.kwargs_fixed:
            kwargs['shapelet_beta'] = args[i]
            i += 1
        if self.kwargs_options.get('add_clump', False):
            if not 'theta_E_clump' in self.kwargs_fixed:
                kwargs['theta_E_clump'] = args[i]
                i += 1
            if not 'r_trunc' in self.kwargs_fixed:
                kwargs['r_trunc'] = args[i]
                i += 1
            if not 'x_clump' in self.kwargs_fixed:
                kwargs['x_clump'] = args[i]
                i += 1
            if not 'y_clump' in self.kwargs_fixed:
                kwargs['y_clump'] = args[i]
                i += 1
        if self.kwargs_options.get('psf_iteration', False):
            if not 'point_amp' in self.kwargs_fixed:
                n = self.num_images - 1
                point_amp = np.append(1, args[i:i+n])
                kwargs['point_amp'] = point_amp
                i += n
        return kwargs, i

    def setParams(self, kwargs):
        """

        :param kwargs:
        :return:
        """
        args = []
        if not 'ra_pos' in self.kwargs_fixed:
            x_pos = kwargs['ra_pos']
            for i in x_pos:
                args.append(i)
        if not 'dec_pos' in self.kwargs_fixed:
            y_pos = kwargs['dec_pos']
            for i in y_pos:
                args.append(i)
        if self.kwargs_options.get('image_plane_source', False):
            if not 'source_pos_image_ra' in self.kwargs_fixed:
                args.append(kwargs['source_pos_image_ra'])
            if not 'source_pos_image_dec' in self.kwargs_fixed:
                args.append(kwargs['source_pos_image_dec'])
        if self.external_shear:
            if not 'gamma1' in self.kwargs_fixed or not 'gamma2' in self.kwargs_fixed:
                args.append(kwargs['gamma1'])
                args.append(kwargs['gamma2'])
        if self.foreground_shear:
            if not 'gamma1_foreground' in self.kwargs_fixed or not 'gamma2_foreground' in self.kwargs_fixed:
                args.append(kwargs['gamma1_foreground'])
                args.append(kwargs['gamma2_foreground'])
        if self.kwargs_options.get('time_delay', False) is True:
            if not 'delay_dist' in self.kwargs_fixed:
                args.append(kwargs['delay_dist'])
        if not 'shapelet_beta' in self.kwargs_fixed:
            args.append(kwargs['shapelet_beta'])

        if self.kwargs_options.get('add_clump', False):
            if not 'theta_E_clump' in self.kwargs_fixed:
                args.append(kwargs['theta_E_clump'])
            if not 'r_trunc' in self.kwargs_fixed:
                args.append(kwargs['r_trunc'])
            if not 'x_clump' in self.kwargs_fixed:
                args.append(kwargs['x_clump'])
            if not 'y_clump' in self.kwargs_fixed:
                args.append(kwargs['y_clump'])
        if self.kwargs_options.get('psf_iteration', False):
            if not 'point_amp' in self.kwargs_fixed:
                point_amp = kwargs['point_amp']
                for i in point_amp[1:]:
                    args.append(i)
        return args

    def add2fix(self, kwargs_fixed):
        """

        :param kwargs_fixed:
        :return:
        """
        fix_return = {}
        if 'ra_pos' in kwargs_fixed:
            fix_return['ra_pos'] = kwargs_fixed['ra_pos']
        if 'dec_pos' in kwargs_fixed:
            fix_return['dec_pos'] = kwargs_fixed['dec_pos']
        if self.kwargs_options.get('image_plane_source', False):
            if 'source_pos_image_ra' in kwargs_fixed:
                fix_return['source_pos_image_ra'] = kwargs_fixed['source_pos_image_ra']
            if 'source_pos_image_dec' in kwargs_fixed:
                fix_return['source_pos_image_dec'] = kwargs_fixed['source_pos_image_dec']
        if self.external_shear:
            if 'gamma1' in kwargs_fixed:
                fix_return['gamma1'] = kwargs_fixed['gamma1']
            if 'gamma2' in kwargs_fixed:
                fix_return['gamma2'] = kwargs_fixed['gamma2']

        if self.foreground_shear:
            if 'gamma1_foreground' in kwargs_fixed:
                fix_return['gamma1_foreground'] = kwargs_fixed['gamma1_foreground']
            if 'gamma2_foreground' in kwargs_fixed:
                fix_return['gamma2_foreground'] = kwargs_fixed['gamma2_foreground']

        if 'delay_dist' in kwargs_fixed:
            fix_return['delay_dist'] = kwargs_fixed['delay_dist']
        if self.kwargs_options.get('time_delay', False) is True:
            if 'delay_dist' in kwargs_fixed:
                fix_return['delay_dist'] = kwargs_fixed['delay_dist']
        if 'shapelet_beta' in kwargs_fixed:
            fix_return['shapelet_beta'] = kwargs_fixed['shapelet_beta']

        if self.kwargs_options.get('add_clump', False):
            if 'theta_E_clump' in kwargs_fixed:
                fix_return['theta_E_clump'] = kwargs_fixed['theta_E_clump']
            if 'r_trunc' in kwargs_fixed:
                fix_return['r_trunc'] = kwargs_fixed['r_trunc']
            if 'x_clump' in kwargs_fixed:
                fix_return['x_clump'] = kwargs_fixed['x_clump']
            if 'y_clump' in kwargs_fixed:
                fix_return['y_clump'] = kwargs_fixed['y_clump']
        if self.kwargs_options.get('psf_iteration', False):
            if 'point_amp' in kwargs_fixed:
                fix_return['point_amp'] = kwargs_fixed['point_amp']
        return fix_return

    def param_init(self, kwargs_mean):
        """

        :param kwargs_mean:
        :return:
        """
        mean, sigma = [], []
        if not 'ra_pos' in self.kwargs_fixed:
            x_pos_mean = kwargs_mean['ra_pos']
            pos_sigma = kwargs_mean['pos_sigma']
            for i in x_pos_mean:
                mean.append(i)
                sigma.append(pos_sigma)
        if not 'dec_pos' in self.kwargs_fixed:
            y_pos_mean = kwargs_mean['dec_pos']
            pos_sigma = kwargs_mean['pos_sigma']
            for i in y_pos_mean:
                mean.append(i)
                sigma.append(pos_sigma)
        if self.kwargs_options.get('image_plane_source', False):
            if not 'source_pos_image_ra' in self.kwargs_fixed:
                mean.append(kwargs_mean['source_pos_image_ra'])
                sigma.append(kwargs_mean['source_pos_image_ra_sigma'])
            if not 'source_pos_image_dec' in self.kwargs_fixed:
                mean.append(kwargs_mean['source_pos_image_dec'])
                sigma.append(kwargs_mean['source_pos_image_dec_sigma'])
        if self.external_shear:
            if not 'gamma1' in self.kwargs_fixed or not 'gamma2' in self.kwargs_fixed:
                mean.append(kwargs_mean['gamma1'])
                mean.append(kwargs_mean['gamma2'])
                shear_sigma = kwargs_mean['shear_sigma']
                sigma.append(shear_sigma)
                sigma.append(shear_sigma)
        if self.foreground_shear:
            if not 'gamma1_foreground' in self.kwargs_fixed or not 'gamma2_foreground' in self.kwargs_fixed:
                mean.append(kwargs_mean['gamma1_foreground'])
                mean.append(kwargs_mean['gamma2_foreground'])
                shear_sigma = kwargs_mean['shear_foreground_sigma']
                sigma.append(shear_sigma)
                sigma.append(shear_sigma)
        if self.kwargs_options.get('time_delay', False) is True:
            if not 'delay_dist' in self.kwargs_fixed:
                mean.append(kwargs_mean['delay_dist'])
                sigma.append(kwargs_mean['delay_dist_sigma'])
        if not 'shapelet_beta' in self.kwargs_fixed:
            mean.append(kwargs_mean['shapelet_beta'])
            sigma.append(kwargs_mean['shapelet_beta_sigma'])

        if self.kwargs_options.get('add_clump', False):
            if not 'theta_E_clump' in self.kwargs_fixed:
                mean.append(kwargs_mean['theta_E_clump'])
                sigma.append(kwargs_mean['theta_E_clump_sigma'])
            if not 'r_trunc' in self.kwargs_fixed:
                mean.append(kwargs_mean['r_trunc'])
                sigma.append(kwargs_mean['r_trunc_sigma'])
            if not 'x_clump' in self.kwargs_fixed:
                mean.append(kwargs_mean['x_clump'])
                sigma.append(kwargs_mean['x_clump_sigma'])
            if not 'y_clump' in self.kwargs_fixed:
                mean.append(kwargs_mean['y_clump'])
                sigma.append(kwargs_mean['y_clump_sigma'])
        if self.kwargs_options.get('psf_iteration', False):
            if not 'point_amp' in self.kwargs_fixed:
                for i in range(1, len(kwargs_mean['point_amp'])):
                    mean.append(kwargs_mean['point_amp'][i])
                    sigma.append(kwargs_mean['point_amp_sigma'])
        return mean, sigma

    def param_bound(self):
        """

        :return:
        """
        low, high = [], []
        if not 'ra_pos' in self.kwargs_fixed:
            pos_low = -10
            pos_high = 10
            for i in range(self.num_images):
                low.append(pos_low)
                high.append(pos_high)
        if not 'dec_pos' in self.kwargs_fixed:
            pos_low = -10
            pos_high = 10
            for i in range(self.num_images):
                low.append(pos_low)
                high.append(pos_high)
        if self.kwargs_options.get('image_plane_source', False):
            if not 'source_pos_image_ra' in self.kwargs_fixed:
                low.append(-10)
                high.append(10)
            if not 'source_pos_image_dec' in self.kwargs_fixed:
                low.append(-10)
                high.append(10)
        if self.external_shear:
            if not 'gamma1' in self.kwargs_fixed or not 'gamma2' in self.kwargs_fixed:
                low.append(-0.8)
                high.append(0.8)
                low.append(-0.8)
                high.append(0.8)
        if self.foreground_shear:
            if not 'gamma1_foreground' in self.kwargs_fixed or not 'gamma2_foreground' in self.kwargs_fixed:
                low.append(-0.8)
                high.append(0.8)
                low.append(-0.8)
                high.append(0.8)
        if self.kwargs_options.get('time_delay', False) is True:
            if not 'delay_dist' in self.kwargs_fixed:
                low.append(0)
                high.append(10000)
        if not 'shapelet_beta' in self.kwargs_fixed:
            low.append(0.01)
            high.append(1)
        if self.kwargs_options.get('add_clump', False):
            if not 'theta_E_clump' in self.kwargs_fixed:
                low.append(0)
                high.append(1)
            if not 'r_trunc' in self.kwargs_fixed:
                low.append(0.001)
                high.append(1)
            if not 'x_clump' in self.kwargs_fixed:
                low.append(-10)
                high.append(10)
            if not 'y_clump' in self.kwargs_fixed:
                low.append(-10)
                high.append(10)
        if self.kwargs_options.get('psf_iteration', False):
            if not 'point_amp' in self.kwargs_fixed:
                for i in range(3):
                    low.append(0)
                    high.append(10)
        return low, high

    def num_param(self):
        """

        :return:
        """
        num = 0
        list = []
        if not 'ra_pos' in self.kwargs_fixed:
            num += self.num_images  # Warning: must be 4 point source positions!!!
            for i in range(self.num_images):
                list.append('ra_pos')
        if not 'dec_pos' in self.kwargs_fixed:
            num += self.num_images
            for i in range(self.num_images):
                list.append('dec_pos')
        if self.kwargs_options.get('image_plane_source', False):
            if not 'source_pos_image_ra' in self.kwargs_fixed:
                num += 1
                list.append('source_pos_image_ra')
            if not 'source_pos_image_dec' in self.kwargs_fixed:
                num += 1
                list.append('source_pos_image_dec')
        if self.external_shear:
            if not 'gamma1' in self.kwargs_fixed or not 'gamma2' in self.kwargs_fixed:
                num += 2
                list.append('shear_1')
                list.append('shear_2')
        if self.foreground_shear:
            if not 'gamma1_foreground' in self.kwargs_fixed or not 'gamma2_foreground' in self.kwargs_fixed:
                num += 2
                list.append('shear_foreground_1')
                list.append('shear_foreground_2')
        if self.kwargs_options.get('time_delay', False) is True:
            if not 'delay_dist' in self.kwargs_fixed:
                num += 1
                list.append('delay_dist')
        if not 'shapelet_beta' in self.kwargs_fixed:
            num += 1
            list.append('shapelet_beta')
        if self.kwargs_options.get('add_clump', False):
            if not 'theta_E_clump' in self.kwargs_fixed:
                num += 1
                list.append('theta_E_clump')
            if not 'r_trunc' in self.kwargs_fixed:
                num += 1
                list.append('r_trunc')
            if not 'x_clump' in self.kwargs_fixed:
                num += 1
                list.append('x_clump')
            if not 'y_clump' in self.kwargs_fixed:
                num += 1
                list.append('y_clump')
        if self.kwargs_options.get('psf_iteration', False):
            if not 'point_amp' in self.kwargs_fixed:
                num += 3
                for i in range(3):
                    list.append('point_amp')
        return num, list