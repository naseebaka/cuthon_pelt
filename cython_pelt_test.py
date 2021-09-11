from nessaid_cli.cmd import NessaidCmd


import time
import pstats
import cProfile
import ruptures as rpt
import matplotlib.pylab as plt


from cython_pelt.pelt import Pelt as CythonPelt
from ruptures import Pelt as Pelt

from nessaid_cli.tokens import StringToken, RangedIntToken


class CythonTestCmd(NessaidCmd):
    r"""
    token MODEL_STR StringToken();
    token MIN_SIZE RangedIntToken(1, 10);
    token JUMP RangedIntToken(1, 10);
    token N RangedIntToken(1, 1000);
    token N_BKPS RangedIntToken(1, 10);
    token DIM RangedIntToken(1, 10);
    token SIGMA RangedIntToken(1, 10);
    token PEN RangedIntToken(1, 10);
    """

    def get_token_classes(self):
        return [
            StringToken,
            RangedIntToken
        ]

    def getPelt(self, cython=False):
        if cython is True:
            return CythonPelt
        else:
            return Pelt

    async def do_pelt(self, cython, profile, model, min_size, jump, n, n_bkps, dim, sigma, pen):
        r"""
        <<
            $cython = False;
            $model = "l2";
            $min_size = 3;
            $jump = 5;
            $n = 50;
            $n_bkps = 3;
            $dim = 1;
            $sigma = 1;
            $pen = 3;
            $profile = True;
        >>
        "pelt-test"
        {
            {
                "use-cython"
                << $cython = True; >>
            },
            {
                "no-profiling"
                << $profile = False; >>
            },
            {
                "model"
                MODEL_STR
                << $model = $2; >>
            },
            {
                "min-size"
                MIN_SIZE
                << $min_size = $2; >>
            },
            {
                "jump"
                JUMP
                << $jump = $2; >>
            },
            {
                "n": "In thousands"
                N
                << $n = $2; >>
            },
            {
                "n-bkps"
                N_BKPS
                << $n_bkps = $2; >>
            },
            {
                "dim"
                DIM
                << $dim = $2; >>
            },
            {
                "sigma"
                SIGMA
                << $sigma = $2; >>
            },
            {
                "pen"
                PEN
                << $pen = $2; >>
            }
        }
        """
        n *= 1000

        print(f"Testing with: cython={cython}, profiling={profile}, model={model}, n={n}, min_size={min_size}, jump={jump}, n_bkps={n_bkps}, dim={dim}, pen={pen}, sigma={sigma}")

        if profile:
            with cProfile.Profile() as pr:
                signal, _ = rpt.pw_constant(n, dim, n_bkps, noise_std=sigma)
                algo = self.getPelt(cython)(model=model, min_size=min_size, jump=jump)
                start = time.time()
                my_bkps = algo.fit_predict(signal, pen=3)
                end = time.time()
                stats = pstats.Stats(pr)
                stats.sort_stats('cumtime')
                stats.print_stats()
        else:
            signal, _ = rpt.pw_constant(n, dim, n_bkps, noise_std=sigma)
            algo = self.getPelt(cython)(model=model, min_size=min_size, jump=jump)
            start = time.time()
            my_bkps = algo.fit_predict(signal, pen=3)
            end = time.time()

        print("Start time:", start)
        print("End time:", end)
        print("Time taken:", end - start)

        await self.show_graph(signal, my_bkps)

    async def show_graph(self, signal, bkps):
        rpt.display(signal, range(len(bkps)), bkps, figsize=(10, 6))
        plt.show()

    def do_exit(self):
        r"""
        "exit"
        """
        self.exit_loop()

    def do__system_info(self):
        # Suppressing the system-info CLI
        pass






if __name__ == '__main__':
    CythonTestCmd(prompt="cython-pelt # ", disable_default_hooks=True).run()