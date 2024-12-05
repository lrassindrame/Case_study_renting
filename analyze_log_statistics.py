import os
import pm4py

def load_xes_files(directory):
    xes_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.xes')]
    return xes_files

# Compute statistics
def extract_statistics(log):
    stats = {}
    # Compute the number of cases/traces
    number_of_traces = log.shape[0]
    stats['number_of_traces'] = number_of_traces

    # Compute the number of events log
    num_events = sum(len(trace) for trace in log)
    stats['number_of_events'] = num_events

    # Compute the number of variants log
    variants = pm4py.stats.get_variants(log)
    num_variants = len(variants)
    stats['number_of_variants'] = num_variants

    # Compute the number of activities log
    activities = pm4py.get_event_attribute_values(log, "concept:name")
    num_activities = len(activities)
    stats['number_of_activities'] = num_activities

    # Start activity
    start_activities = pm4py.get_start_activities(log)
    stats['start_activities'] = start_activities

    # End activity
    end_activities = pm4py.get_end_activities(log)
    stats['end_activities'] = end_activities

    # Compute the number of activities per variant (ex: variant1 : 4 activities)
    count_activities_per_variant = log.groupby("case:concept:name")["activity"].nunique()
    stats['count_activities_per_variant'] = count_activities_per_variant

    # Compute the event log trace per variant (ex: variant1 : a,b,c,d)
    activities_per_variant = log.groupby("case:concept:name")["activity"].apply(list)
    stats['activities_per_variant'] = activities_per_variant

    # Compute the average number of activities per case
    avg_activities_per_case = log.groupby("case:concept:name")["activity"].count().mean()
    stats['avg_activities_per_case'] = avg_activities_per_case

    # Compute the minimum and maximum number of activities per case
    min_activities_per_case = min(log.groupby("case:concept:name")["activity"].count())
    max_activities_per_case = max(log.groupby("case:concept:name")["activity"].count())
    stats['min_activities_per_case'] = min_activities_per_case
    stats['max_activities_per_case'] = max_activities_per_case

    # Compute the minimum, maximum, and average case duration
    case_durations = pm4py.get_all_case_durations(log)
    stats['min_case_duration'] = min(case_durations)
    stats['max_case_duration'] = max(case_durations)
    stats['avg_case_duration'] = sum(case_durations) / float(len(case_durations))

    # Compute statistics using resources
    resource_stats = log['resource'].value_counts()
    stats['resource_stats'] = resource_stats

    # Life cycle status counts: number of occurrences of each status
    cycle_time = pm4py.get_cycle_time(log)
    stats['cycle_time'] = cycle_time

    # Identifies activities that have rework occurrences, i.e., activities that occur more than once within the same case
    # or.. rework = pm4py.get_variants_as_tuples(log)
    rework = pm4py.get_rework_cases_per_activity(log)
    stats['rework'] = rework

    # # Analyze the distribution of the case durations
    # case_durations = pm4py.get_all_case_durations(log)
    # stats['case_durations'] = case_durations

    # Analyze cluster log
    # pm4py.analysis.cluster_log.get_k_means(log, 4)
    
    return stats

def main():
    directory = 'datasets'
    xes_files = load_xes_files(directory)
    
    for xes_file in xes_files:
        log = pm4py.read_xes(xes_file)
        stats = extract_statistics(log)

        skip_keys = ["case_durations", "activities_per_variant"]
        
        print(f"Statistics for {xes_file}:")
        for key, value in stats.items():
            if str(key) in skip_keys :
                continue
            print(f"{key}: {value}")
            print("-"*25) # separator between statistics
        print("="*25+"\n") # separator between files

if __name__ == "__main__":
    main()