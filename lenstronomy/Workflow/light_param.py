import astrofunc.util as util

class LightParam(object):
    """

    """

    def __init__(self, kwargs_options, kwargs_fixed, type='lens_light'):
        self.kwargs_options = kwargs_options
        self.kwargs_fixed = kwargs_fixed
        if type == 'lens_light':
            self.model_list = kwargs_options['lens_light_model_list']
            self._fix_center = False
        elif type == 'source_light':
            self.model_list = kwargs_options['source_light_model_list']
            if self.kwargs_options.get('solver', False):
                self._fix_center = True
            else:
                self._fix_center = False
        else:
            raise ValueError("type %s not supported." % type)
        self.type = type

    def getParams(self, args, i):
        """

        :param args:
        :param i:
        :return:
        """
        kwargs_list = []
        for k, model in enumerate(self.model_list):
            kwargs = {}
            kwargs_fixed = self.kwargs_fixed[k]
            if not self._fix_center or k > 0:
                if not 'center_x' in kwargs_fixed:
                    kwargs['center_x'] = args[i]
                    i += 1
                if not 'center_y' in kwargs_fixed:
                    kwargs['center_y'] = args[i]
                    i += 1
            if model in ['SHAPELETS']:
                if not 'beta' in kwargs_fixed:
                    kwargs['beta'] = args[i]
                    i += 1
            if model in ['SERSIC', 'CORE_SERSIC', 'SERSIC_ELLIPSE', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_sersic' in kwargs_fixed:
                    kwargs['I0_sersic'] = args[i]
                    i += 1
                if not 'n_sersic' in kwargs_fixed:
                    kwargs['n_sersic'] = args[i]
                    i += 1
                if not 'R_sersic' in kwargs_fixed:
                    kwargs['R_sersic'] = args[i]
                    i += 1

            if model in ['SERSIC_ELLIPSE', 'CORE_SERSIC', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'phi_G' in kwargs_fixed or not 'q' in kwargs_fixed:
                    phi, q = util.elliptisity2phi_q(args[i], args[i+1])
                    kwargs['phi_G'] = phi
                    kwargs['q'] = q
                    i += 2
            if model in ['DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_2' in kwargs_fixed:
                    kwargs['I0_2'] = args[i]
                    i += 1
                if not 'R_2' in kwargs_fixed:
                    kwargs['R_2'] = args[i]
                    i += 1
                if not 'n_2' in kwargs_fixed:
                    kwargs['n_2'] = args[i]
                    i += 1
            if model in ['CORE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'Rb' in kwargs_fixed:
                    kwargs['Rb'] = args[i]
                    i += 1
                if not 'gamma' in kwargs_fixed:
                    kwargs['gamma'] = args[i]
                    i += 1
            kwargs_list.append(kwargs)
        return kwargs_list, i

    def setParams(self, kwargs_list):
        """

        :param kwargs:
        :return:
        """
        args = []
        for k, model in enumerate(self.model_list):
            kwargs = kwargs_list[k]
            kwargs_fixed = self.kwargs_fixed[k]
            if not self._fix_center or k > 0:
                if not 'center_x' in kwargs_fixed:
                    args.append(kwargs['center_x'])
                if not 'center_y' in kwargs_fixed:
                    args.append(kwargs['center_y'])
            if model in ['SHAPELETS']:
                if not 'beta' in kwargs_fixed:
                    args.append(kwargs['beta'])
            if model in ['SERSIC', 'CORE_SERSIC', 'SERSIC_ELLIPSE', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_sersic' in kwargs_fixed:
                    args.append(kwargs['I0_sersic'])
                if not 'n_sersic' in kwargs_fixed:
                    args.append(kwargs['n_sersic'])
                if not 'R_sersic' in kwargs_fixed:
                    args.append(kwargs['R_sersic'])

            if model in ['SERSIC_ELLIPSE', 'CORE_SERSIC', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'phi_G' in kwargs_fixed or not 'q' in kwargs_fixed:
                        e1, e2 = util.phi_q2_elliptisity(kwargs['phi_G'], kwargs['q'])
                        args.append(e1)
                        args.append(e2)
            if model in ['DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_2' in kwargs_fixed:
                    args.append(kwargs['I0_2'])
                if not 'R_2' in kwargs_fixed:
                    args.append(kwargs['R_2'])
                if not 'n_2' in kwargs_fixed:
                    args.append(kwargs['n_2'])
            if model in ['CORE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'Rb' in kwargs_fixed:
                    args.append(kwargs['Rb'])
                if not 'gamma' in kwargs_fixed:
                    args.append(kwargs['gamma'])
        return args

    def add2fix(self, kwargs_fixed_list):
        """

        :param kwargs_fixed:
        :return:
        """
        fix_return_list = []
        for k, model in enumerate(self.model_list):
            kwargs_fixed = kwargs_fixed_list[k]
            fix_return = {}
            if not self._fix_center or k > 0:
                if 'center_x' in kwargs_fixed:
                    fix_return['center_x'] = kwargs_fixed['center_x']
                if 'center_y' in kwargs_fixed:
                    fix_return['center_y'] = kwargs_fixed['center_y']
            if model in ['SHAPELETS']:
                if 'beta' in kwargs_fixed:
                    fix_return['beta'] = kwargs_fixed['beta']
            if model in ['SERSIC', 'CORE_SERSIC', 'SERSIC_ELLIPSE', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if 'I0_sersic' in kwargs_fixed:
                    fix_return['I0_sersic'] = kwargs_fixed['I0_sersic']
                if 'n_sersic' in kwargs_fixed:
                    fix_return['n_sersic'] = kwargs_fixed['n_sersic']
                if 'R_sersic' in kwargs_fixed:
                    fix_return['R_sersic'] = kwargs_fixed['R_sersic']

            if model in ['SERSIC_ELLIPSE', 'CORE_SERSIC', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if 'phi_G' in kwargs_fixed or 'q' in kwargs_fixed:
                        fix_return['phi_G'] = kwargs_fixed['phi_G']
                        fix_return['q'] = kwargs_fixed['q']

            if model in ['DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if 'I0_2' in kwargs_fixed:
                    fix_return['I0_2'] = kwargs_fixed['I0_2']
                if 'R_2' in kwargs_fixed:
                    fix_return['R_2'] = kwargs_fixed['R_2']
                if 'n_2' in kwargs_fixed:
                    fix_return['n_2'] = kwargs_fixed['n_2']

            if model in ['CORE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if 'Rb' in kwargs_fixed:
                    fix_return['Rb'] = kwargs_fixed['Rb']
                if 'gamma' in kwargs_fixed:
                    fix_return['gamma'] = kwargs_fixed['gamma']
            fix_return_list.append(fix_return)
        return fix_return_list

    def param_init(self, kwargs_mean_list):
        """

        :param kwargs_mean:
        :return:
        """
        mean = []
        sigma = []
        for k, model in enumerate(self.model_list):
            kwargs_mean = kwargs_mean_list[k]
            kwargs_fixed = self.kwargs_fixed[k]
            if not self._fix_center or k > 0:
                if not 'center_x' in kwargs_fixed:
                    mean.append(kwargs_mean['center_x'])
                    sigma.append(kwargs_mean['center_x_sigma'])
                if not 'center_y' in kwargs_fixed:
                    mean.append(kwargs_mean['center_y'])
                    sigma.append(kwargs_mean['center_y_sigma'])
            if model in ['SHAPELETS']:
                if not 'beta' in kwargs_fixed:
                    mean.append(kwargs_mean['beta'])
                    sigma.append(kwargs_mean['beta_sigma'])
            if model in ['SERSIC', 'CORE_SERSIC', 'SERSIC_ELLIPSE', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_sersic' in kwargs_fixed:
                    mean.append(kwargs_mean['I0_sersic'])
                    sigma.append(kwargs_mean['I0_sersic_sigma'])
                if not 'n_sersic' in kwargs_fixed:
                    mean.append(kwargs_mean['n_sersic'])
                    sigma.append(kwargs_mean['n_sersic_sigma'])
                if not 'R_sersic' in kwargs_fixed:
                    mean.append(kwargs_mean['R_sersic'])
                    sigma.append(kwargs_mean['R_sersic_sigma'])

            if model in ['SERSIC_ELLIPSE', 'CORE_SERSIC', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'phi_G' in kwargs_fixed or not 'q' in kwargs_fixed:
                        phi = kwargs_mean['phi_G']
                        q = kwargs_mean['q']
                        e1,e2 = util.phi_q2_elliptisity(phi, q)
                        mean.append(e1)
                        mean.append(e2)
                        ellipse_sigma = kwargs_mean['ellipse_sigma']
                        sigma.append(ellipse_sigma)
                        sigma.append(ellipse_sigma)

            if model in ['DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_2' in kwargs_fixed:
                    mean.append(kwargs_mean['I0_2'])
                    sigma.append(kwargs_mean['I0_2_sigma'])
                if not 'R_2' in kwargs_fixed:
                    mean.append(kwargs_mean['R_2'])
                    sigma.append(kwargs_mean['R_2_sigma'])
                if not 'n_2' in kwargs_fixed:
                    mean.append(kwargs_mean['n_2'])
                    sigma.append(kwargs_mean['n_2_sigma'])

            if model in ['CORE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'Rb' in kwargs_fixed:
                    mean.append(kwargs_mean['Rb'])
                    sigma.append(kwargs_mean['Rb_sigma'])
                if not 'gamma' in kwargs_fixed:
                    mean.append(kwargs_mean['gamma'])
                    sigma.append(kwargs_mean['gamma_sigma'])
            return mean, sigma

    def param_bound(self):
        """

        :return:
        """
        low = []
        high = []
        for k, model in enumerate(self.model_list):
            kwargs_fixed = self.kwargs_fixed[k]
            if not self._fix_center or k > 0:
                if not 'center_x' in kwargs_fixed:
                    low.append(-60)
                    high.append(60)
                if not 'center_y' in kwargs_fixed:
                    low.append(-60)
                    high.append(60)
            if model in ['SHAPELETS']:
                if not 'beta' in kwargs_fixed:
                    low.append(0.000001)
                    high.append(60)
            if model in ['SERSIC', 'CORE_SERSIC', 'SERSIC_ELLIPSE', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_sersic' in kwargs_fixed:
                    low.append(0)
                    high.append(100)
                if not 'n_sersic' in kwargs_fixed:
                    low.append(0.2)
                    high.append(10)
                if not 'R_sersic' in kwargs_fixed:
                    low.append(0.01)
                    high.append(3)

            if model in ['SERSIC_ELLIPSE', 'CORE_SERSIC', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'phi_G' in kwargs_fixed or not 'q' in kwargs_fixed:
                        low.append(-0.8)
                        high.append(0.8)
                        low.append(-0.8)
                        high.append(0.8)

            if model in ['DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_2' in kwargs_fixed:
                    low.append(0)
                    high.append(100)
                if not 'R_2' in kwargs_fixed:
                    low.append(0.01)
                    high.append(30)
                if not 'n_2' in kwargs_fixed:
                    low.append(0.2)
                    high.append(30)

            if model in ['CORE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'Rb' in kwargs_fixed:
                    low.append(0.01)
                    high.append(30)
                if not 'gamma' in kwargs_fixed:
                    low.append(-3)
                    high.append(3)
        return low, high

    def num_param(self):
        """

        :return:
        """
        num = 0
        list = []
        for k, model in enumerate(self.model_list):
            kwargs_fixed = self.kwargs_fixed[k]
            if not self._fix_center or k > 0:
                if not 'center_x' in kwargs_fixed:
                    num+=1
                    list.append(str('center_x_'+self.type))
                if not 'center_y' in kwargs_fixed:
                    num+=1
                    list.append(str('center_y_'+self.type))
            if model in ['SHAPELETS']:
                if not 'beta' in kwargs_fixed:
                    num += 1
                    list.append(str('beta_'+self.type))
            if model in ['SERSIC', 'CORE_SERSIC', 'SERSIC_ELLIPSE', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_sersic' in kwargs_fixed:
                    num += 1
                    list.append(str('I0_sersic_'+self.type))
                if not 'n_sersic' in kwargs_fixed:
                    num += 1
                    list.append(str('n_sersic_'+self.type))
                if not 'R_sersic' in kwargs_fixed:
                    num += 1
                    list.append(str('R_sersic_'+self.type))

            if model in ['SERSIC_ELLIPSE', 'CORE_SERSIC', 'DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'phi_G' in kwargs_fixed or not 'q' in kwargs_fixed:
                        num += 2
                        list.append(str('e1_'+self.type))
                        list.append(str('e2_' + self.type))

            if model in ['DOUBLE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'I0_2' in kwargs_fixed:
                    num += 1
                    list.append(str('I2_'+self.type))
                if not 'R_2' in kwargs_fixed:
                    num += 1
                    list.append(str('R_2_'+self.type))
                if not 'n_2' in kwargs_fixed:
                    num += 1
                    list.append(str('n_2_'+self.type))

            if model in ['CORE_SERSIC', 'DOUBLE_CORE_SERSIC']:
                if not 'Rb' in kwargs_fixed:
                    num += 1
                    list.append(str('Rb_'+self.type))
                if not 'gamma' in kwargs_fixed:
                    num += 1
                    list.append(str('gamma_'+self.type))
        return num, list