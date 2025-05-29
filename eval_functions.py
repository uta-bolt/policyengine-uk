def povertycalc(baseline, eval_year, reformed):
    # Step 1: Calculate in_poverty for everyone
    baseline_pov = baseline.calculate(
        "in_relative_poverty_ahc", eval_year, map_to="person", use_weights=True
    )
    ages = baseline.calculate("age", eval_year)
    weights = baseline.get_weights("age", eval_year)
    # Step 2: Create mask for children (age < 16 or < 18 as appropriate)
    is_child = ages < 16  # or < 18 depending on definition
    # Step 3: Get child-level poverty status and weights
    child_poverty = baseline_pov[is_child]
    child_weights = weights[is_child]
    # Step 4: Calculate total number and percent of children in poverty
    num_children = child_weights.sum()
    num_children_in_poverty = (child_poverty).sum()
    percent_in_poverty = num_children_in_poverty / num_children
    # print(f"Number of children: {num_children:,.0f} in {eval_year}, baseline")
    # print(f"Number of children in poverty: {num_children_in_poverty:,.0f}in {eval_year}, baseline")
    # print(f"Percent of children in poverty: {percent_in_poverty:.2%}in {eval_year}, baseline")

    # Step 1: Calculate in_poverty for everyone
    baseline_pov = reformed.calculate(
        "in_relative_poverty_ahc", eval_year, map_to="person", use_weights=True
    )
    ages = reformed.calculate("age", eval_year)
    weights = reformed.get_weights("age", eval_year)
    # Step 2: Create mask for children (age < 16 or < 18 as appropriate)
    is_child = ages < 16  # or < 18 depending on definition
    # Step 3: Get child-level poverty status and weights
    child_poverty = baseline_pov[is_child]
    child_weights = weights[is_child]
    # Step 4: Calculate total number and percent of children in poverty
    num_children = child_weights.sum()
    num_children_in_poverty_after = (child_poverty).sum()
    percent_in_poverty_after = num_children_in_poverty_after / num_children
    # print(f"Number of children: {num_children:,.0f} in {eval_year}, reformed")
    # print(f"Number of children in poverty: {num_children_in_poverty_after:,.0f} in {eval_year}, reformed")
    # print(f"Percent of children in poverty: {percent_in_poverty_after:.2%} in {eval_year}, reformed")
    print(
        f"Reduction in child poverty: {num_children_in_poverty - num_children_in_poverty_after:,.0f} in {eval_year}, reformed"
    )


def avg_gain_gainer(baseline, reformed, eval_year):
    net_income_baseline = baseline.calculate("household_net_income", eval_year)
    net_income_reformed = reformed.calculate("household_net_income", eval_year)
    diff = (
        net_income_reformed * net_income_reformed.weights
        - net_income_baseline * net_income_baseline.weights
    )
    gainers = (diff > 0).sum()
    total = net_income_reformed.sum() - net_income_baseline.sum()
    print(f"Avg gain of gainers {eval_year}: {total/gainers}")
