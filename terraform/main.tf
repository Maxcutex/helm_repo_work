locals {
  full_bucket_name = "${var.repository_name}-${var.bucket_name}"
}

resource "aws_s3_bucket" "helm-chart-repository" {
  bucket = "${local.full_bucket_name}"

  # Allows read access to objects not uploaded by the bucket owner; see <https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteAccessPermissionsReqd.html> for details
  acl = "public-read"

  force_destroy = "${var.is_forcing_destroy}"

  versioning {
    enabled = "${var.is_versioning_enabled}"
  }

  tags = {
    Terraform             = true
    Helm-Chart-Repository = true
  }
}

data "aws_iam_policy_document" "helm-chart-repository-policy-document" {
  # Minimum permission required for website access; see <https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteAccessPermissionsReqd.html> for details
  statement {
    sid    = "bucket"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions   = ["s3:ListBucket",]
    resources = ["${aws_s3_bucket.helm-chart-repository.arn}", "${aws_s3_bucket.helm-chart-repository.arn}/*"]
  }

  statement {
    sid    = "files"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions   = ["s3:PutObjectAcl",
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:DeleteObject"]
    resources = ["${aws_s3_bucket.helm-chart-repository.arn}", "${aws_s3_bucket.helm-chart-repository.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "helm-chart-repository-bucket-policy" {
  bucket = "${aws_s3_bucket.helm-chart-repository.id}"
  policy = "${data.aws_iam_policy_document.helm-chart-repository-policy-document.json}"
}
