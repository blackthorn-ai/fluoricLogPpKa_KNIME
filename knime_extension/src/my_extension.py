import logging
import math

import pandas as pd
import knime.extension as knext

from nodes.fluoric_logp import Fluoriclogp
from nodes.fluoric_pka import Fluoricpka

LOGGER = logging.getLogger(__name__)
