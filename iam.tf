resource "aws_iam_role" "ssm_patch_role" {
  name = "Lambda_SSM_patching_alerts"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
  EOF
}

resource "aws_iam_role_policy" "patch_list_accounts" {
  name = "${aws_iam_role.ssm_patch_role.name}-lambda-role"
  role = aws_iam_role.ssm_patch_role.name

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:ap-southeast-2:${data.aws_caller_identity.current.account_id}:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssm:ListCommandInvocations",
                "ses:SendRawEmail"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}