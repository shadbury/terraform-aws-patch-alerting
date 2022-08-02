resource "aws_cloudwatch_event_target" "targets" {
    target_id = "target"
    arn       = aws_lambda_function.ssm_alerts_function.arn
    rule      = aws_cloudwatch_event_rule.event_rules.name
}

resource "aws_cloudwatch_event_rule" "event_rules" {
  name        = "patch_alert_scan"
  description = "Rule for alert scanning"
  schedule_expression = "cron(0 8 ? * mon *)"
}