resource "aws_lambda_function" "ssm_alerts_function" {
  function_name = "ssm_patching_alerts"
  role          = aws_iam_role.ssm_patch_role.arn
  handler       = "ssm_patching_alerts.lambda_handler"
  runtime       = "python3.8"
  filename      = "ssm_patching_alerts.zip"
  source_code_hash = "${data.archive_file.zipit.output_base64sha256}"

  environment {
    variables = {
      RECIPIENTS  = var.patch_alerting_recepients
      SENDER      = var.patch_alerting_sender
      SUBJECT     = "Patch runcommand Failure - ${var.profile}"
    }
  }
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.ssm_alerts_function.id}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.event_rules.arn}"
}