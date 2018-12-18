import os

from pm4py.algo.other.simple.model.tracelog import factory as simple_extraction_factory
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.stochastic_petri import map as stochastic_map
from pm4py.statistics.traces.tracelog.case_arrival import get_case_arrival_avg
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.objects.stochastic_petri.lp_perf_bounds import LpPerfBounds


log_name = os.path.join("tests", "input_data", "running-example.xes")
log = xes_importer.apply(log_name)
# obtain a simple, sound workflow net, containing only visibile unique transitions,
# applying the Alpha Miner to some of the top variants (methods by Ale)
net, initial_marking, final_marking = simple_extraction_factory.apply(log, classic_output=True)
# visualize the output Petri net
gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
pn_vis_factory.view(gviz)
# gets the average time between cases starts
avg_time_starts = get_case_arrival_avg(log)
print("avg_time_starts=", avg_time_starts)
# gets the stochastic distribution associated to the Petri net and the log
smap = stochastic_map.get_map_from_log_and_net(log, net, initial_marking, final_marking,
                                               force_distribution="EXPONENTIAL")
print("smap=", smap)
perf_bound_obj = LpPerfBounds(net, initial_marking, final_marking, smap, avg_time_starts)
net1, imarking1, fmarking1 = perf_bound_obj.get_net()
gviz = pn_vis_factory.apply(net1, imarking1, fmarking1)
pn_vis_factory.view(gviz)